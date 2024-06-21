import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer

from black_friday.constants import TARGET_COLUMN, SCHEMA_FILE_PATH
from black_friday.entity.config_entity import DataTransformationConfig
from black_friday.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from black_friday.exception import BlackFridayException
from black_friday.logger import logging
from black_friday.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
# from black_friday.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise BlackFridayException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise BlackFridayException(e, sys)

    
    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logging.info("Got numerical cols from schema config")

            class LabelEncoderTransformer(BaseEstimator, TransformerMixin):
                def __init__(self):
                    self.label_encoder = LabelEncoder()

                def fit(self, X, y=None):
                    self.label_encoder.fit(X.squeeze())
                    return self

                def transform(self, X):
                    return self.label_encoder.transform(X.squeeze()).reshape(-1, 1)
            age_list = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']    
            oh_encoder = OneHotEncoder(drop='first')
            ordinal_encoder = OrdinalEncoder(categories=[age_list])
            most_frequent_imputer = SimpleImputer(strategy='most_frequent')

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            lab_columns= self._schema_config['lab_columns']
            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            impute_columns = self._schema_config['impute_columns']
            
            preprocessor = ColumnTransformer(
                [
                    ("Label", LabelEncoderTransformer(), lab_columns),
                    ("Onehot", oh_encoder, oh_columns),
                    ("Ordinal", ordinal_encoder, or_columns),
                    ("Imputer", most_frequent_imputer, impute_columns)
                ]
            )
            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor

        except Exception as e:
            raise BlackFridayException(e, sys) from e


    def initiate_data_transformation(self, ) -> DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]

                logging.info("Got train features and test features of Training dataset")

                input_feature_train_df['Stay_In_Current_City_Years'] = input_feature_train_df['Stay_In_Current_City_Years'].str.replace("+", "", regex=False)

                input_feature_train_df['Stay_In_Current_City_Years'] = input_feature_train_df['Stay_In_Current_City_Years'].astype(int)

                logging.info("Transformed ans changed data type of stay column to the Training dataset")

                drop_cols = self._schema_config['drop_columns']

                logging.info("drop the columns in drop_cols of Training dataset")

                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                
                # target_feature_train_df = target_feature_train_df.replace(
                #     TargetValueMapping()._asdict()
                # )


                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

                target_feature_test_df = test_df[TARGET_COLUMN]

                input_feature_test_df['Stay_In_Current_City_Years'] = input_feature_test_df['Stay_In_Current_City_Years'].str.replace("+", "", regex=False)

                input_feature_test_df['Stay_In_Current_City_Years'] = input_feature_test_df['Stay_In_Current_City_Years'].astype(int)

                logging.info("Transformed ans changed data type of stay column to the Training dataset")

                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)

                logging.info("drop the columns in drop_cols of Test dataset")

                # target_feature_test_df = target_feature_test_df.replace(
                # TargetValueMapping()._asdict()
                # )

                logging.info("Got train features and test features of Testing dataset")

                logging.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )

                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

                logging.info(
                    "Used the preprocessor object to fit transform the train features"
                )

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")

                # logging.info("Applying SMOTEENN on Training dataset")

                # smt = SMOTEENN(sampling_strategy="minority")

                # input_feature_train_final, target_feature_train_final = smt.fit_resample(
                #     input_feature_train_arr, target_feature_train_df
                # )

                # logging.info("Applied SMOTEENN on training dataset")

                # logging.info("Applying SMOTEENN on testing dataset")

                # input_feature_test_final, target_feature_test_final = smt.fit_resample(
                #     input_feature_test_arr, target_feature_test_df
                # )

                # logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")

                train_arr = np.c_[
                    input_feature_train_arr, np.array(target_feature_train_df)
                ]

                test_arr = np.c_[
                    input_feature_test_arr, np.array(target_feature_test_df)
                ]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)

        except Exception as e:
            raise BlackFridayException(e, sys) from e