import csv
import os
from volcengine_ml_platform.dataloader.dataset import VeDataset


class PointCloudDataset(VeDataset):
    def __init__(self, root_dir, dataset_meta, loader, transformer_fn=None, annotation_fn=None, ):
        super().__init__(root_dir, dataset_meta, loader, transformer_fn=transformer_fn, annotation_fn=annotation_fn)

    def load_meta_info(self):
        csv_path = self.parse_index_path()
        with open(csv_path) as csv_file:
            spamreader = csv.reader(csv_file)
            for row in spamreader:
                self.samples.append(row)
            self.samples = self.samples[1:]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        sample = self.samples[index]
        src, result = self.pre_process(sample[0], sample[3])
        return (src, result)

    def pre_process(self, src, result):
        src = self.pre_process_src(src)
        label = self.pre_process_result(result)
        return (src, label)

    def pre_process_src(self, resource):
        urls = resource.split(',')
        contents = []
        for i in range(len(urls)):
            file_path = os.path.join(self.root_dir, urls[i].replace("tos://", ""))
            content = self.loader_fn(file_path)
            if self.transformer_fn is not None:
                content = self.transformer_fn(content)
            contents.append(content)
        return contents

    def pre_process_result(self, result):
        if self.annotation_fn is not None:
            return self.annotation_fn(result)
        return result
