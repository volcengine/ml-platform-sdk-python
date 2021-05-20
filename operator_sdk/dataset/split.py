import json
import logging
import math
import os
import shutil

import numpy as np


def move_dataset(metadata, input_dir, output_dir):
    file_path = metadata['data']['filePath']
    file_dir, file_name = os.path.split(file_path)
    target_dir = os.path.join(output_dir,
                              os.path.relpath(file_dir, start=input_dir))

    # create output file directory
    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError:
        logging.warning('Cannot create directory: %s', target_dir)

    target_file = os.path.join(target_dir, file_name)
    shutil.copy(file_path, target_file)
    metadata['data']['filePath'] = target_file

    # store metadata
    with open(os.path.join(output_dir, 'local_metadata.manifest'),
              'w+') as meta_file:
        line = json.dumps(metadata)
        meta_file.write(line)


def split_dataset(input_dir,
                  training_dir,
                  testing_dir,
                  ratio=0.8,
                  random_state=0):
    line_count = 0
    with open(os.path.join(input_dir, 'local_metadata.manifest')) as f:
        for line in f:
            line_count = line_count + 1

    np.random.seed(random_state)
    test_index_set = set(
        np.random.choice(line_count,
                         math.floor(line_count * (1 - ratio)),
                         replace=False))
    index = 0
    with open(os.path.join(input_dir, 'local_metadata.manifest')) as f:
        for line in f:
            manifest_line = json.loads(line)
            if index in test_index_set:
                move_dataset(manifest_line, input_dir, testing_dir)
            else:
                move_dataset(manifest_line, input_dir, training_dir)
            index = index + 1
