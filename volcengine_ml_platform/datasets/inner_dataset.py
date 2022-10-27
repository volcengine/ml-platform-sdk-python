# type: ignore
import logging
import os
from typing import Optional

from volcengine import Credentials

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.datasets.dataset import _Dataset
from volcengine_ml_platform.datasets.dataset_util import dataset_dict
from volcengine_ml_platform.datasets.tabular_dataset import TabularDataset
from volcengine_ml_platform.innerapi import dataset_client as inner_dataset_client
from volcengine_ml_platform.innerapi import sts_token
from volcengine_ml_platform.io import tos
from volcengine_ml_platform.openapi import secure_token_client


class InnerDataset(TabularDataset):
    def __init__(
        self,
        dataset_type,
        dataset_id: str = "",
        annotation_id: Optional[str] = None,
        local_path: str = ".",
        tos_source: Optional[str] = None,
        target_user_id=None,
        target_account_id=None,
    ):
        _Dataset.__init__(self, dataset_id, annotation_id,
                          local_path, tos_source)
        # new info
        self.dataset_type = dataset_type
        self.target_user_id = (
            int(target_user_id) if target_user_id is not None else None
        )
        self.target_account_id = (
            int(target_account_id) if target_account_id is not None else None
        )
        self.module_name = constant.MODULE_DATASET
        self.inner_dataset_client = inner_dataset_client.InnerDatasetClient()
        self.inner_sts_client = sts_token.STSApiClient()
        self.secure_token_client = secure_token_client.SecureTokenClient()

    def set_target_account_id(self, target_account_id):
        self.target_account_id = target_account_id

    def set_target_user_id(self, target_user_id):
        self.target_user_id = target_user_id

    def get_target_account_id(self):
        if self.target_account_id is None:
            self.target_account_id = int(
                os.getenv(constant.ACCOUNT_ID_ENV_NAME))
        return self.target_account_id

    def get_target_user_id(self):
        if self.target_user_id is None:
            self.target_user_id = int(os.getenv(constant.USER_ID_ENV_NAME))
        return self.target_user_id

    def _get_secure_token(self):
        resp = self.secure_token_client.admin_get_secure_token(
            time_to_live=600,
            account_id=self.get_target_account_id(),
            user_id=self.get_target_user_id(),
        )
        return resp["Result"]["Token"]

    def _get_sts_token(self):
        resp = self.inner_sts_client.get_sts_token(self._get_secure_token())
        result = resp["Result"]
        return result["AccessKeyId"], result["SecretAccessKey"], result["SessionToken"]

    def _get_tos_client(self):
        ak, sk, session_token = self._get_sts_token()
        region = volcengine_ml_platform.get_credentials().region
        credentials = Credentials.Credentials(
            ak, sk, constant.SERVICE_NAME, region)
        return tos.TOSClient(credentials, session_token)

    def _get_dataset_detail(self):
        if not self.dataset_id:
            logging.warning(
                "data which don't have dataset id can't get dataset detail",
            )
            return
        try:
            self.detail = self.inner_dataset_client.get_dataset(
                dataset_id=self.dataset_id,
                token=self._get_secure_token(),
            )["Result"]
            self.data_count = self.detail["NonTabularDataCount"]
        except Exception as e:
            logging.error("get datasets detail failed, error: %s", e)
            raise Exception("invalid datasets") from e

    def _get_annotation_detail(self):
        if self.annotation_id is None:
            logging.warning(
                "data which don't have annotation dataset id can't get annotation dataset detail",
            )
            return
        try:
            resp = self.inner_dataset_client.get_annotation_set(
                dataset_id=self.dataset_id,
                annotation_id=self.annotation_id,
                token=self._get_secure_token(),
            )
            self.annotation_detail = resp["Result"]
        except Exception as e:
            logging.error("get annotation detail failed, error: %s", e)
            raise Exception("invalid annotation") from e

    def _download_file(self, tos_url: str, file_path: str):
        self.tos_client = self._get_tos_client()
        return super()._download_file(tos_url, file_path)

    def _create_non_manifest_dataset(self):
        self.tos_client = self._get_tos_client()
        super()._create_non_manifest_dataset()

    def _create_manifest_dataset(
        self,
        manifest_keyword: str,
        limit=-1,
    ):
        self.tos_client = self._get_tos_client()
        super()._create_manifest_dataset(manifest_keyword, limit)

    def download(self, local_path: str = "InnerDataset", limit=-1):
        if local_path:
            self.local_path = local_path
        if self.dataset_type == TabularDataset:
            self._create_non_manifest_dataset()
        else:
            self._create_manifest_dataset(
                manifest_keyword=dataset_dict.get(self.dataset_type),
            )

    def split(
        self,
        dataset_type,
        training_dir: str,
        testing_dir: str,
        ratio=0.8,
        random_state=0,
    ):
        if self.dataset_type == TabularDataset:
            return super().split(
                training_dir,
                testing_dir,
                ratio=ratio,
                random_state=random_state,
            )

        else:
            return super().split_dataset(
                dataset_type,
                training_dir,
                testing_dir,
                ratio=ratio,
                random_state=random_state,
            )
