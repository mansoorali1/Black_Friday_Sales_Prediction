from black_friday.cloud_storage.aws_storage import SimpleStorageService
from black_friday.exception import BlackFridayException
from black_friday.entity.estimator import BlackFridayModel
import sys
from pandas import DataFrame
from black_friday.logger import logging


class BlackFridayEstimator:
    """
    This class is used to save and retrieve black_fridays model in s3 bucket and to do prediction
    """

    def __init__(self,bucket_name,model_path,):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model:BlackFridayModel=None


    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except BlackFridayException as e:
            print(e)
            return False

    def load_model(self,)->BlackFridayModel:
        """
        Load the model from the model_path
        :return:
        """

        return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)

    def save_model(self,from_file,remove:bool=False)->None:
        """
        Save the model to the model_path
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        :return:
        """
        try:
            self.s3.upload_file(from_file,
                                to_filename=self.model_path,
                                bucket_name=self.bucket_name,
                                remove=remove
                                )
        except Exception as e:
            raise BlackFridayException(e, sys)


    def predict(self,dataframe:DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            logging.info(f"bucket name and model path: {self.bucket_name,self.model_path}")

            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise BlackFridayException(e, sys)