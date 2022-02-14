import argparse
import json

from volcengine_ml_platform.models import model


def register_model(client, args):
    tensor_config = None
    with open(args.tensor_config) as f:
        tensor_config = json.load(f)

    resp = client.register(
        model_name=args.model_name,
        model_format=args.model_format,
        model_type=args.model_type,
        local_path=args.local_path,
        remote_path=args.remote_path,
        tensor_config=tensor_config,
    )
    print(resp)
    return resp["Result"]["ModelID"], resp["Result"]["VersionInfo"]["ModelVersion"]


def deploy_model(client, args, model_id, model_version):
    inference_service = client.deploy(
        model_id=model_id,
        model_version=model_version,
        service_name=args.service_name,
        flavor=args.flavor,
        replica=args.replica,
        resource_group_id=args.resource_group_id,
        image_id=args.image_id,
    )
    inference_service.print()


def main():
    parser = argparse.ArgumentParser(description="Model upload example")

    parser.add_argument(
        "--local-path",
        type=str,
        default=None,
        help="local storage path of the model",
    )
    parser.add_argument(
        "--remote-path",
        type=str,
        default=None,
        help="remote storage path of the model, e.g.: tos path",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="cifar-demo-model",
        help="model name",
    )
    parser.add_argument(
        "--model-format",
        type=str,
        default="TorchScript",
        help="model format, values in SavedModel, GraphDef, TorchScript, TensorRT, ONNX, CaffeModel, "
        + "NetDef, MXNetParams, Scikit_Learn, XGBoost, LightGBM, MATX, Custom",
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="PyTorch:1.7",
        help="model framework name and framework version, format: <framework-name>:<framework-version>, "
        + "for example: TensorFlow:2.0 Framework values limited in "
        + "TensorFlow, PyTorch, TensorRT, ONNX, Caffe, Caffe2, MXNet, Scikit_Learn, XGBoost, LightGBM, MATX, Custom",
    )
    parser.add_argument(
        "--tensor-config",
        type=str,
        default="tensor_config.json",
        help="model tensor config file",
    )
    parser.add_argument(
        "--enable-deploy",
        type=bool,
        default=True,
        help="deploy the model once it is registered successfully",
    )
    parser.add_argument(
        "--service-name",
        type=str,
        default="cifar-demo-service",
        help="service name",
    )
    parser.add_argument(
        "--flavor",
        type=str,
        default="ml.g1e.2xlarge",
        help="flavor",
    )
    parser.add_argument(
        "--replica",
        type=int,
        default=1,
        help="inferece service replica",
    )
    parser.add_argument(
        "--resource-group-id",
        type=str,
        default=None,
        help="resource group id",
    )
    parser.add_argument(
        "--image-id",
        type=str,
        default="ml_platform/tritonserver:21.02",
        help="image id",
    )

    args = parser.parse_args()

    client = model.Model()
    model_id, model_version = register_model(client, args)

    if args.enable_deploy:
        deploy_model(client, args, model_id, model_version)


if __name__ == "__main__":
    main()
