import os

from operator_sdk.dataset.split import split_dataset

input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'test_import/d-20210512141706-mckhc')
training_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'train_set')
testing_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'test_set')

if __name__ == '__main__':
    split_dataset(input_dir, training_dir, testing_dir)
