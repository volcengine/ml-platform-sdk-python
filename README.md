# ML Platform Python SDK 使用手册

机器学习平台提供了 Python SDK `volcengine-ml-platform` 供用户在任何网络通畅的机器上访问机器学习平台，该 SDK 当前支持模型注册、服务部署、实验管理等功能。

## 相关概念

- [AK / SK]()
- [Region]()
- [命令行工具（volc）]()

## 安装

可以通过如下指令安装最新版本的 SDK：

```shell
git clone http://github.com/volcengine/ml-platform-sdk-python
cd ml-platform-sdk-python && python -m pip install .
```

## 配置 AK / SK

在正式使用 SDK 之前需要先完成火山引擎账号的 AK / SK 的本地配置，否则在使用 SDK 访问机器学习平台时无法通过身份校验。

1. 登录火山引擎控制台并前往【密钥管理】查看当前账号的 AK / SK。
  - 若当前账号为子账号，需要具备 `AccessKeyFullAccess` 的 IAM 策略。
2. 配置 AK / SK 推荐使用 volc 命令行工具。同 SDK 一样，该工具也是一种脱离控制台页面访问机器学习平台的方式。该工具的安装详见命令行工具（volc），完成命令行工具的安装后通过 `volc configure` 交互地配置 AK / SK 及 region。

```shell
volc configure
volc access key [********yM2I]:           填写用户的 AK
volc secret access key [********TQ==]:    填写用户的 SK
volc region [cn-beijing]: █              填写所在地域，目前仅支持 cn-beijing
```

  - 方式 2：若不想额外安装命令行工具，可在 `~/.volc` 目录下手动创建 `config` 及 `credentials` 两个文件并正确填写 region 及 AK / SK。
```ini
# ~/.volc/config

[default]
region       = cn-beijing           填写所在地域，目前仅支持 cn-beijing
```

```ini
# ~/.volc/credentials

[default]
access_key_id     = ******          填写用户的 AK
secret_access_key = ******          填写用户的 SK
```

  - 方式 3：通过环境变量配置 AK / SK 及 region。
```shell
export VOLC_ACCESSKEY=****          填写用户的 AK
export VOLC_SECRETKEY=****          填写用户的 SK
export VOLC_REGION=****             填写所在地域，目前仅支持 cn-beijing
```

## 使用 SDK

如何使用 SDK 访问机器学习平台，完成模型注册、服务部署、实验管理等操作详见如下示例。

- 模型管理与服务部署：
  - [示例代码](https://github.com/volcengine/ml-platform-sdk-python/tree/main/samples)
- 实验管理：
  - [README](https://github.com/volcengine/ml-platform-sdk-python/tree/main/volcengine_ml_platform/tracking/README.md)
  - [示例代码](https://github.com/volcengine/ml-platform-sdk-python/tree/main/samples/tracking)
