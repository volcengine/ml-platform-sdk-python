import json
import logging
import math
import os
import shutil

import numpy as np


def move_dataset(metadata, meta_type, input_dir, output_dir):
    for data in metadata:
        file_path = data['filePath']
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
        data['filePath'] = target_file

    # store metadata
    with open(os.path.join(output_dir, 'metadata.json'), 'w+') as meta_file:
        json.dump({meta_type: metadata}, meta_file)


def split_dataset(input_dir,
                  training_dir,
                  testing_dir,
                  ratio=0.8,
                  random_state=0):
    with open(os.path.join(input_dir, 'metadata.json')) as f:
        meta_json = json.load(f)
        meta_type = None
        if 'image_meta' in meta_json:
            meta_type = 'image_meta'
        elif 'video_meta' in meta_json:
            meta_type = 'video_meta'
        else:
            meta_type = 'text_meta'
        metadata = meta_json[meta_type]

        np.random.seed(random_state)
        np.random.shuffle(metadata)

        split_index = math.floor(len(metadata) * ratio)
        training_metadata = metadata[:split_index]
        testing_metadata = metadata[split_index:]

    move_dataset(training_metadata, meta_type, input_dir, training_dir)
    move_dataset(testing_metadata, meta_type, input_dir, testing_dir)
