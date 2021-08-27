import json
from typing import Dict
from typing import List
from typing import Optional

from volcengine_ml_platform.annotation.ttypes import AnnotationDataType


def get_annotation_section(annotation_line):
    return annotation_line['Annotation']


def get_content(annotation_line):
    data = annotation_line['Data']
    with open(data['FilePath'], mode='rb', encoding='utf-8') as fd:
        content = fd.read()
        return content


def get_data_section(annotation_line):
    return annotation_line['Data']


class Annotation:
    """
    annotation object
    """

    def __init__(self, manifest_file: Optional[str] = None):
        self.manifest_file = manifest_file
        self.label_index: Dict[str, List] = {}
        self.annotation_data: List[str] = []
        self.iter_index = 0
        self._build_label_index()

    def __len__(self):
        return len(self.annotation_data)

    def get_by_label(self, label):
        return self.label_index.get(label, [])

    def extract(self, index):
        """get annotation of the index line
        Args:
            index of annotation_data
        Return:
            content of image/text
            annotation of data, diff data has diff struct
        """
        if index < 0 or index >= len(self.annotation_data):
            raise Exception('out of range')
        manifest_data = self.annotation_data[index]
        return self.extract_annotation_with_data(manifest_data)

    def extract_annotation(self, manifest_line):
        annotation = get_annotation_section(manifest_line)
        return annotation

    def extract_annotation_with_data(self, manifest_line):
        """get content and annotation
        Args:
            manifest line data
        Return:
            content of image/text
            annotation of data, diff data has diff struct
        """
        content = get_content(manifest_line)
        annotation = self.extract_annotation(manifest_line)
        return {'content': content, 'annotation': annotation}

    def _get_labels(self, annotation_result):
        """
        Args:
            manifest_result data
        Return:
            annotation labels
        """
        labels = []
        for data in annotation_result['Data']:
            data_type = data['Type']
            if data_type in (
                    AnnotationDataType.SingleSelector,
                    AnnotationDataType.BlankFilling,
            ):
                labels.append(data['Label'])
            elif data_type == AnnotationDataType.MultipleSelector:
                labels.extend(data['Labels'])
        return labels

    def _build_label_index(self):
        with open(self.manifest_file, encoding='utf-8') as fd:
            for manifest_line in fd:
                manifest_data = json.loads(manifest_line.strip('\n'))
                self.annotation_data.append(manifest_data)
                annotation = get_annotation_section(manifest_data)
                for result in annotation['Result']:
                    labels = self._get_labels(result)
                    for label in labels:
                        match_record = self.label_index.get(label, [])
                        match_record.append(manifest_data)
                        self.label_index[label] = match_record
