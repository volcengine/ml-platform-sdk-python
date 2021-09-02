# Copyright (c) 2018-2019, NVIDIA CORPORATION
# Copyright (c) 2017-      Facebook, Inc
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# import os
from functools import partial

import numpy as np
import torch
import torchvision.transforms as transforms
from image_classification.autoaugment import AutoaugmentImageNetPolicy
from PIL import Image

from volcengine_ml_platform.datasets.image_dataset import ImageDataset

try:
    import env

    env.init()
except Exception:
    pass

DATA_BACKEND_CHOICES = ["pytorch", "syntetic"]


def fast_collate(memory_format, batch):
    imgs = [img[0] for img in batch]
    targets = torch.tensor([target[1] for target in batch], dtype=torch.int64)
    w = imgs[0].size()[0]
    h = imgs[0].size()[1]
    tensor = torch.zeros((len(imgs), 3, h, w), dtype=torch.uint8).contiguous(
        memory_format=memory_format
    )
    for i, img in enumerate(imgs):
        nump_array = np.asarray(img, dtype=np.uint8)
        if nump_array.ndim < 3:
            nump_array = np.expand_dims(nump_array, axis=-1)
        nump_array = np.rollaxis(nump_array, 2)

        tensor[i] += torch.from_numpy(nump_array.copy())

    return tensor, targets


def expand(num_classes, dtype, tensor):
    e = torch.zeros(
        tensor.size(0), num_classes, dtype=dtype, device=torch.device("cuda")
    )
    e = e.scatter(1, tensor.unsqueeze(1), 1.0)
    return e


class PrefetchedWrapper:
    def prefetched_loader(loader, num_classes, one_hot):
        mean = (
            torch.tensor([0.485 * 255, 0.456 * 255, 0.406 * 255])
            .cuda()
            .view(1, 3, 1, 1)
        )
        std = (
            torch.tensor([0.229 * 255, 0.224 * 255, 0.225 * 255])
            .cuda()
            .view(1, 3, 1, 1)
        )

        stream = torch.cuda.Stream()
        first = True
        input, target = None, None
        for next_input, next_target in loader:
            with torch.cuda.stream(stream):
                next_input = next_input.cuda(non_blocking=True)
                next_target = next_target.cuda(non_blocking=True)
                next_input = next_input.float()
                if one_hot:
                    next_target = expand(num_classes, torch.float, next_target)

                next_input = next_input.sub_(mean).div_(std)

            if not first:
                yield input, target
            else:
                first = False

            torch.cuda.current_stream().wait_stream(stream)
            input = next_input
            target = next_target

        yield input, target

    def __init__(self, dataloader, start_epoch, num_classes, one_hot):
        self.dataloader = dataloader
        self.epoch = start_epoch
        self.one_hot = one_hot
        self.num_classes = num_classes

    def __iter__(self):
        if self.dataloader.sampler is not None and isinstance(
            self.dataloader.sampler, torch.utils.data.distributed.DistributedSampler
        ):

            self.dataloader.sampler.set_epoch(self.epoch)
        self.epoch += 1
        return PrefetchedWrapper.prefetched_loader(
            self.dataloader, self.num_classes, self.one_hot
        )

    def __len__(self):
        return len(self.dataloader)


def get_pytorch_train_loader(
    data_path,
    image_size,
    batch_size,
    num_classes,
    one_hot,
    interpolation="bilinear",
    augmentation=None,
    start_epoch=0,
    workers=5,
    _worker_init_fn=None,
    memory_format=torch.contiguous_format,
):
    interpolation = {"bicubic": Image.BICUBIC, "bilinear": Image.BILINEAR}[
        interpolation
    ]
    # traindir = os.path.join(data_path, "train")
    transforms_list = [
        transforms.RandomResizedCrop(image_size, interpolation=interpolation),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ]
    if augmentation == "autoaugment":
        transforms_list.append(AutoaugmentImageNetPolicy())
    if torch.distributed.is_initialized():
        rank = torch.distributed.get_rank()
        world_size = torch.distributed.get_world_size()
        # device_id = rank % torch.cuda.device_count()
    else:
        rank = 0
        world_size = 1
        # device_id = 0

    tos_source = data_path
    transform_ = transforms.Compose(transforms_list)

    def transform(data):
        data = transform_(data)
        data = data.permute(1, 2, 0)
        return data

    def target_transform(target):
        target = int(target["Result"][0]["Data"][0]["Label"])
        return target

    train_dataset = ImageDataset(
        tos_source=tos_source,
        local_path="./demo_train_manifest",
    )
    train_dataset = train_dataset.init_torch_dataset(
        transform=transform,
        target_transform=target_transform,
    )
    if torch.distributed.is_initialized():
        train_sampler = torch.utils.data.distributed.DistributedSampler(
            train_dataset, num_replicas=world_size, rank=rank, shuffle=True
        )
    else:
        train_sampler = None

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        sampler=train_sampler,
        batch_size=batch_size,
        shuffle=(train_sampler is None),
        num_workers=16,  # workers,
        worker_init_fn=_worker_init_fn,
        pin_memory=True,
        collate_fn=partial(fast_collate, memory_format),
        drop_last=True,
        persistent_workers=True,
    )

    return (
        PrefetchedWrapper(train_loader, start_epoch, num_classes, one_hot),
        len(train_loader),
    )


def get_pytorch_val_loader(
    data_path,
    image_size,
    batch_size,
    num_classes,
    one_hot,
    interpolation="bilinear",
    workers=5,
    _worker_init_fn=None,
    crop_padding=32,
    memory_format=torch.contiguous_format,
):
    interpolation = {"bicubic": Image.BICUBIC, "bilinear": Image.BILINEAR}[
        interpolation
    ]

    tos_source = data_path
    transform_ = transforms.Compose(
        [
            transforms.Resize(image_size + crop_padding, interpolation=interpolation),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
        ]
    )

    def transform(data):
        data = transform_(data)
        data = data.permute(1, 2, 0)
        return data

    def target_transform(target):
        target = int(target["Result"][0]["Data"][0]["Label"])
        return target

    val_dataset = ImageDataset(
        tos_source=tos_source,
        local_path="./demo_val_manifest",
    )
    val_dataset = val_dataset.init_torch_dataset(
        transform=transform,
        target_transform=target_transform,
    )

    if torch.distributed.is_initialized():
        val_sampler = torch.utils.data.distributed.DistributedSampler(
            val_dataset, shuffle=False
        )
    else:
        val_sampler = None

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        sampler=val_sampler,
        batch_size=batch_size,
        shuffle=(val_sampler is None),
        num_workers=workers,
        worker_init_fn=_worker_init_fn,
        pin_memory=True,
        collate_fn=partial(fast_collate, memory_format),
        drop_last=False,
        persistent_workers=True,
    )

    return PrefetchedWrapper(val_loader, 0, num_classes, one_hot), len(val_loader)


class SynteticDataLoader:
    def __init__(
        self,
        batch_size,
        num_classes,
        num_channels,
        height,
        width,
        one_hot,
        memory_format=torch.contiguous_format,
    ):
        input_data = (
            torch.randn(batch_size, num_channels, height, width)
            .contiguous(memory_format=memory_format)
            .cuda()
            .normal_(0, 1.0)
        )
        if one_hot:
            input_target = torch.empty(batch_size, num_classes).cuda()
            input_target[:, 0] = 1.0
        else:
            input_target = torch.randint(0, num_classes, (batch_size,))
        input_target = input_target.cuda()

        self.input_data = input_data
        self.input_target = input_target

    def __iter__(self):
        while True:
            yield self.input_data, self.input_target


def get_syntetic_loader(
    data_path,
    image_size,
    batch_size,
    num_classes,
    one_hot,
    interpolation=None,
    augmentation=None,
    start_epoch=0,
    workers=None,
    _worker_init_fn=None,
    memory_format=torch.contiguous_format,
):
    return (
        SynteticDataLoader(
            batch_size,
            num_classes,
            3,
            image_size,
            image_size,
            one_hot,
            memory_format=memory_format,
        ),
        -1,
    )
