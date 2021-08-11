import logging
from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.annotation.image_classification_annotation import ImageClassificationAnnotation
from volcengine_ml_platform.config import credential as auth_credential
import volcengine_ml_platform

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    volcengine_ml_platform.init(auth_credential.Credential(ak, sk, region))
    annotation_set = ImageDataset(annotation_id='da-20210805035908-xvw49',
                                  dataset_id='d-20210805035907-xg2ls')

    annotation_set.create('./flower_classification')

    annotation_set.split(training_dir='./demo_dataset/train',
                         testing_dir='./demo_dataset/test',
                         ratio=0.5)

    annotation = ImageClassificationAnnotation(
        './flower_classification/local_metadata.manifest')

    for i in range(len(annotation)):
        logging.info(annotation.extract(i))

    logging.info(annotation.get_by_label('牵牛花'))
    logging.info(annotation.get_by_label('不认识'))
