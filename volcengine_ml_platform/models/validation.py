import json

import jsonschema

_shape_schema = {"type": "array", "items": {"type": "integer"}, "minItems": 1}

_tensor_schema = {
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
            "enum": [
                "FP32",
                "FP16",
                "INT8",
                "INT16",
                "INT32",
                "INT64",
                "UINT8",
                "UINT16",
                "UINT32",
                "UINT64",
                "FP64",
                "STRING",
            ],
        },
    },
    "required": ["TensorName", "Shape", "DType"],
}

_model_schema = {
    "type": "object",
    "properties": {
        "Inputs": {
            "type": "array",
            "items": _tensor_schema,
        },
        "Outputs": {
            "type": "array",
            "items": _tensor_schema,
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


def validate_tensor_config(tensor_config):
    if tensor_config is None:
        return
    jsonschema.validate(tensor_config, schema=_model_schema)


def validate_metrics(model_metrics):
    if model_metrics is None:
        return
    jsonschema.validate(model_metrics, _model_metrics_schema)
    for metrics in model_metrics:
        valid_json(metrics["Params"])
        valid_json(metrics["MetricsData"])


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

    validate_tensor_config(conf)

    data = [
        {
            "MetricsType": "ImageClassification",
            "Params": '{"hardware": "ml.standard.xlarge"}',
            "MetricsData": '{"qps": 10, "latency": 0.3}',
        },
    ]

    validate_metrics(data)
