import argparse
import datetime
import os
from collections import OrderedDict

import torch
import torch.distributed as dist
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from models import *
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.tensorboard import SummaryWriter

# /data00 为 tos bucket挂载的根目录，以下本地POSIX本地目录/data00/datasets/cifar/ 对应 tos://${your_bucket_name}/datasets/cifar
dataset_path = "/data00/datasets/cifar/"
# 直接将模型训练好的参数，保存到TOS上。下文的/data00/models/cifar/ 对应 tos://${your_bucket_name}/models/cifar
saved_model_dir = "/data00/models/cifar"
log_dir = os.getenv("TENSORBOARD_LOG_PATH", "/tensorboard_logs/")

train_writer = SummaryWriter(os.path.join(log_dir, "train"))
test_writer = SummaryWriter(os.path.join(log_dir, "test"))


def train(model, device, train_loader, optimizer, criterion, epoch, log_interval):
    model.train()
    train_loss = 0
    total_num = 0
    correct_num = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, predicted = output.max(1)
        total_num += target.size(0)
        correct_num += predicted.eq(target).sum().item()
        if batch_idx % log_interval == 0:
            cur_loss = train_loss / (batch_idx + 1)
            acc = 100.0 * correct_num / total_num
            print(
                "Train Epoch: {} [{:>5}/{} ({:.0f}%)]\tLoss: {:.6f}\tAcc: {:.3f}({}/{})".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    train_loss / (batch_idx + 1),
                    acc,
                    correct_num,
                    total_num,
                )
            )
            train_writer.add_scalar("Loss", cur_loss, epoch)
            train_writer.add_scalar("Acc", acc, epoch)
            # grid = torchvision.utils.make_grid(data)
            # writer.add_image('images', grid, global_step=epoch)


def test(model, device, test_loader, criterion, epoch):
    model.eval()
    test_loss = 0
    total_num = 0
    correct_num = 0
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item()
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            total_num += target.size(0)
            correct_num += pred.eq(target.view_as(pred)).sum().item()
    cur_loss = test_loss / (batch_idx + 1)
    acc = 100.0 * correct_num / total_num
    test_writer.add_scalar("Loss", cur_loss, epoch)
    test_writer.add_scalar("Acc", acc, epoch)
    print(
        "\nTest Epoch:{:>5} \tLoss: {:.6f}\tAcc: {:.3f}({}/{})\n".format(
            epoch, cur_loss, acc, correct_num, total_num
        )
    )


def main():
    # Training settings
    parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        metavar="N",
        help="input batch size for training (default: 256)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        metavar="N",
        help="number of epochs to train (default: 100)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        metavar="LR",
        help="learning rate (default: 1.0)",
    )
    parser.add_argument(
        "--no-cuda", action="store_true", default=False, help="disables CUDA training"
    )
    parser.add_argument(
        "--seed", type=int, default=1, metavar="S", help="random seed (default: 1)"
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=10,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument(
        "--save-model",
        action="store_true",
        default=True,
        help="For Saving the current Model",
    )
    parser.add_argument("--local_rank", default=-1, type=int)
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")
    print(f"use device={device}, local_rank={args.local_rank}")

    if args.local_rank >= 0:
        torch.cuda.set_device(args.local_rank)
        dist.init_process_group(backend="nccl")

    train_kwargs = {"batch_size": args.batch_size}
    test_kwargs = {"batch_size": args.batch_size}
    if use_cuda:
        cuda_kwargs = {"num_workers": 1, "pin_memory": True, "shuffle": True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    train_transform = transforms.Compose(
        [
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )

    test_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )
    # Download=False，TOS数据已直接挂载到${dataset_path}目录下，直接读取即可，无需下载
    train_dataset = torchvision.datasets.CIFAR10(
        root=dataset_path, train=True, download=False, transform=train_transform
    )
    test_dataset = torchvision.datasets.CIFAR10(
        root=dataset_path, train=False, download=False, transform=test_transform
    )
    if args.local_rank >= 0:
        sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=128, num_workers=2, sampler=sampler
        )
    else:
        train_loader = torch.utils.data.DataLoader(train_dataset, **train_kwargs)
    test_loader = torch.utils.data.DataLoader(test_dataset, **test_kwargs)

    model = ResNet18().to(device)
    if args.local_rank >= 0:
        model = DDP(model, device_ids=[args.local_rank])

    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.SGD(
        model.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=200)

    for epoch in range(1, args.epochs + 1):
        if args.local_rank >= 0:
            train_loader.sampler.set_epoch(epoch)
        train(
            model, device, train_loader, optimizer, criterion, epoch, args.log_interval
        )
        test(model, device, test_loader, criterion, epoch)
        scheduler.step()

    if args.save_model and (args.local_rank == -1 or dist.get_rank() == 0):
        # TOS挂载带来的限制: 模型保存到TOS上的时候，每次只能保存为一个新文件，不能覆盖已有文件
        global saved_model_dir
        saved_model_dir = "{}/{}".format(
            saved_model_dir, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        )
        os.makedirs(saved_model_dir, exist_ok=True)
        model_path = f"{saved_model_dir}/cifar_demo.pt"

        if args.local_rank == -1:
            model.eval()
            model = torch.jit.script(model)
            torch.jit.save(model, model_path)
        elif dist.get_rank() == 0:
            raw_model = ResNet18().to(device)
            # remove `module.` in state dict, e.g.: module.fc3.bias => fc3.bias
            renamed_state_dict = OrderedDict(
                (k[7:], v) for k, v in model.state_dict().items()
            )
            raw_model.load_state_dict(renamed_state_dict)
            raw_model.eval()
            raw_model = torch.jit.script(raw_model)
            torch.jit.save(raw_model, model_path)
        else:
            pass
        print(f"finish save model to {model_path}")


if __name__ == "__main__":
    main()
