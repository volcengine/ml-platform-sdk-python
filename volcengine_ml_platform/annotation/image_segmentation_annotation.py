from typing import Optional

from volcengine_ml_platform.annotation.annotation import Annotation
from volcengine_ml_platform.annotation.annotation import get_annotation_section
from volcengine_ml_platform.annotation.annotation import get_data_section


class ImageSegmentationAnnotation(Annotation):
    def __init__(self, manifest_file: Optional[str] = None):
        Annotation.__init__(self, manifest_file)

    def _get_url(self, manifest_line):
        data = get_data_section(manifest_line)
        return data['ImageURL']

    def extract_annotation(self, manifest_line):
        annotation = get_annotation_section(manifest_line)

        label_result = []
        for result in annotation['Result']:
            labels = self._get_labels(result)
            if result.get('Bbox') is not None:
                pos = result.get('Bbox')
            elif result.get('Segmentation') is not None:
                pos = result.get('Segmentation')
            label_result.append(
                {
                    'labels': labels,
                    'box': pos,
                },
            )
        return label_result
