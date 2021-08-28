from typing import Optional

from volcengine_ml_platform.annotation.annotation import Annotation
from volcengine_ml_platform.annotation.annotation import get_annotation_section
from volcengine_ml_platform.annotation.annotation import get_data_section


class TextEntitySetAnnotation(Annotation):
    def __init__(self, manifest_file: Optional[str] = None):
        Annotation.__init__(self, manifest_file)

    def _get_url(self, manifest_line):
        data = get_data_section(manifest_line)
        return data["TextUrl"]

    def extract_annotation(self, manifest_line):
        annotation = get_annotation_section(manifest_line)

        label_result = []
        for result in annotation["Result"]:
            labels = self._get_labels(result)
            text_selector = result["Text"]
            label_result.append(
                {"labels": labels, "text_selector": text_selector},
            )
        return label_result
