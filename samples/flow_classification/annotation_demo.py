import logging
import os

from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.annotation.image_classification_annotation import ImageClassificationAnnotation

from samples import env
from volcengine_ml_platform.util import cache_dir

try:
    from samples import env

    env.init()
except ImportError or AttributeError:
    pass

CACHE_DIR = cache_dir.create(
    "flower_classification/swin_transformer_with_annotation")

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    annotation_set = ImageDataset(annotation_id='da-20210805035908-xvw49',
                                  dataset_id='d-20210805035907-xg2ls')

    data_path = CACHE_DIR.subpath("data")
    annotation_set.download(data_path)

    annotation_set.split(training_dir=CACHE_DIR.subpath("train"),
                         testing_dir=CACHE_DIR.subpath("test"),
                         ratio=0.5)

    annotation = ImageClassificationAnnotation(
        os.path.join(data_path, "local_metadata.manifest"))

    for i in range(len(annotation)):
        logging.info(annotation.extract(i))

    logging.info(annotation.get_by_label('牵牛花'))
    logging.info(annotation.get_by_label('不认识'))
