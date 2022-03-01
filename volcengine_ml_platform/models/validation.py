import copy
import json
import os

import jsonschema

SUPPORTED_MODEL_CATEGORY = [
    "TextClassification",
    "TabularClassification",
    "TabularRegression",
    "ImageClassification",
    "TextEntity",
]

SUPPORTED_SOURCE_TYPE = ["TOS", "Local", "AutoML", "Perf"]

_shape_schema = {"type": "array", "items": {"type": "integer"}, "minItems": 1}

_perf_job_supported_tensor_dtype = [
    "FLOAT16",
    "FLOAT",
    "DOUBLE",
    "INT8",
    "INT16",
    "INT32",
    "INT64",
    "UINT8",
    "UINT16",
    "UINT32",
    "UINT64",
]

_model_supported_tensor_dtype = copy.deepcopy(_perf_job_supported_tensor_dtype)
_model_supported_tensor_dtype.extend(["STRING", "BOOL"])

_perf_job_tensor_schema = {
    "type": "object",
    "properties": {
        "TensorName": {"type": "string"},
        "Shape": {
            "type": "object",
            "properties": {
                "MinShape": _shape_schema,
                "MaxShape": _shape_schema,
            },
            "required": ["MinShape", "MaxShape"],
        },
        "DType": {
            "type": "string",
            "enum": _perf_job_supported_tensor_dtype,
        },
    },
    "required": ["TensorName", "Shape", "DType"],
}

_model_tensor_schema = {
    "type": "object",
    "properties": {
        "TensorName": {"type": "string"},
        "Shape": _shape_schema,
        "DType": {
            "type": "string",
            "enum": _model_supported_tensor_dtype,
        },
    },
    "required": ["TensorName", "Shape", "DType"],
}

_perf_job_tensor_config_schema = {
    "type": "object",
    "properties": {
        "Inputs": {
            "type": "array",
            "items": _perf_job_tensor_schema,
        },
        "Outputs": {
            "type": "array",
            "items": _perf_job_tensor_schema,
        },
    },
    "required": ["Inputs"],
}

_model_tensor_config_schema = {
    "type": "object",
    "properties": {
        "Inputs": {
            "type": "array",
            "items": _model_tensor_schema,
        },
        "Outputs": {
            "type": "array",
            "items": _model_tensor_schema,
        },
    },
    "required": ["Inputs"],
}

_metrics_schema = {
    "type": "object",
    "properties": {
        "MetricsType": {
            "type": "string",
            "enum": [
                "ImageClassification",
                "TextClassification",
                "TabularClassification",
                "TabularRegression",
                "TextEntity",
                "Perf",
            ],
        },
        "Params": {"type": "string"},
        "MetricsData": {"type": "string"},
    },
}

_model_metrics_schema = {
    "type": "array",
    "items": _metrics_schema,
    "minItems": 1,
}


def valid_json(serialized_data):
    json.loads(serialized_data)


def validate_model_tensor_config(tensor_config):
    if tensor_config is None:
        return
    try:
        jsonschema.validate(tensor_config, schema=_model_tensor_config_schema)
    except Exception as e:
        raise Exception("Invalid tensor config.") from e


def validate_perf_job_tensor_config(tensor_config):
    jsonschema.validate(tensor_config, schema=_perf_job_tensor_config_schema)


def validate_metrics(model_metrics):
    if model_metrics is None:
        return
    try:
        jsonschema.validate(model_metrics, _model_metrics_schema)
        for metrics in model_metrics:
            valid_json(metrics["Params"])
            valid_json(metrics["MetricsData"])
    except Exception as e:
        raise Exception("Invalid models metrics.") from e


def validate_local_path(local_path):
    if local_path is None:
        raise Exception("Model local_path is empty")
    if not os.path.exists(local_path):
        raise Exception("Model local_path not exists %s", local_path)


def validate_model_category(model_category):
    if model_category is not None and model_category not in SUPPORTED_MODEL_CATEGORY:
        raise Exception(
            "Invalid model_category %s, values should be one of %s",
            model_category,
            SUPPORTED_MODEL_CATEGORY,
        )


def validate_source_type(source_type):
    if source_type is not None and source_type not in SUPPORTED_SOURCE_TYPE:
        raise Exception(
            "Invalid source_type %s, values should be one of %s",
            source_type,
            SUPPORTED_SOURCE_TYPE,
        )


if __name__ == "__main__":
    conf = {
        "Inputs": [
            {
                "TensorName": "input_ids_1:0",
                "DType": "INT32",
                "Shape": {"MaxShape": [8, 256], "MinShape": [1, 256]},
            },
            {
                "TensorName": "input_mask_1:0",
                "DType": "INT32",
                "Shape": {"MaxShape": [8, 256], "MinShape": [1, 256]},
            },
            {
                "TensorName": "segment_ids_1:0",
                "DType": "INT32",
                "Shape": {"MaxShape": [8, 256], "MinShape": [1, 256]},
            },
        ],
    }

    validate_perf_job_tensor_config(conf)

    data = [
        {
            "MetricsType": "ImageClassification",
            "Params": '{"hardware": "ml.standard.xlarge"}',
            "MetricsData": '{"qps": 10, "latency": 0.3}',
        },
    ]

    validate_metrics(data)
