from ml_platform_sdk.inference.inference_service import InferenceService


class VersionInfo:
    """
    Version info of a Model
    """

    def __init__(self,
                 version_id: str,
                 version_index: str,
                 path: str,
                 source_type: str,
                 model_format: str,
                 model_type: str,
                 description=None):
        self.version_id = version_id
        self.version_index = version_index
        self.format = model_format
        self.type = model_type
        self.path = path
        self.description = description
        self.source_type = source_type

        self.service_id = None


class Model:
    """
    Model class contains the information about the entity registered
    in the model repository.
    A model can have multiple versions, but only one version will be
    stored in a Model.
    """

    def __init__(self,
                 model_id: str,
                 model_name: str,
                 version_id: str,
                 version_index: str,
                 path: str,
                 source_type: str,
                 model_format: str,
                 model_type: str,
                 description=None) -> None:
        self.model_id = model_id
        self.model_name = model_name
        self.version_info = VersionInfo(version_id=version_id,
                                        version_index=version_index,
                                        model_format=model_format,
                                        model_type=model_type,
                                        description=description,
                                        path=path,
                                        source_type=source_type)

    def deploy(self,
               ak: str,
               sk: str,
               region: str,
               service_name: str,
               image_url: str,
               flavor_id: str,
               env=None,
               replica=1,
               description=None):
        """deploy model as inference_service

        Args:
            ak (str): access key
            sk (str): secret key
            region (str): service region
            service_name (str): [description]
            image_url (str): [description]
            flavor_id (str): inference machine standard id
            env (list, optional): environment variables. Defaults to None.
            replica (int, optional): number of instance replicas. Defaults to 1.
            description (str, optional): description of service. Defaults to None.
        """
        inference_service = InferenceService(region)
        inference_service.set_ak(ak)
        inference_service.set_sk(sk)

        if self.service_id is None:
            res = inference_service.create_service(service_name=service_name,
                                                   model=self,
                                                   image_url=image_url,
                                                   flavor_id=flavor_id,
                                                   env=env,
                                                   replica=replica,
                                                   description=description)
            self.service_id = res['Result']['ServiceID']
            inference_service.start_service(self.service_id)
        else:
            raise Exception('Inference service has been deployed')

    def undeploy(self, ak: str, sk: str, region: str):
        if self.service_id:
            inference_service = InferenceService(region)
            inference_service.set_ak(ak)
            inference_service.set_sk(sk)

            inference_service.stop_service(self.service_id)
            inference_service.delete_service(self.service_id)
            self.service_id = None
        else:
            raise Exception('Inference service is not deployed')

    # TODO
    def predict(self):
        pass

    def batch_predict(self):
        pass

    def explain(self):
        pass
