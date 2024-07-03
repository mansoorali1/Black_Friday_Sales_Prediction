import os
import sys

import numpy as np
import pandas as pd
from black_friday.entity.config_entity import BlackFridayPredictorConfig
from black_friday.entity.s3_estimator import BlackFridayEstimator
from black_friday.exception import BlackFridayException
from black_friday.logger import logging
from black_friday.utils.main_utils import read_yaml_file
from pandas import DataFrame


class BlackFridayData:
    def __init__(self,
                gender,
                age,
                occupation,
                city_category,
                stay_in_current_city_years,
                marital_status,
                product_category_1,
                product_category_2,
                product_category_3
                ):
        """
        BlackFriday Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.gender = gender
            self.age = age
            self.occupation = occupation
            self.city_category = city_category
            self.stay_in_current_city_years = stay_in_current_city_years
            self.marital_status = marital_status
            self.product_category_1 = product_category_1
            self.product_category_2 = product_category_2
            self.product_category_3 = product_category_3
              
        except Exception as e:
            raise BlackFridayException(e, sys) from e

    def get_blackfriday_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from BlackFriday class input
        """
        try:
            
            blackfriday_input_dict = self.get_blackfriday_data_as_dict()
            logging.info(f"black friday dict: {blackfriday_input_dict}")
            df = DataFrame(blackfriday_input_dict)


            return df
        
        except Exception as e:
            raise BlackFridayException(e, sys) from e


    def get_blackfriday_data_as_dict(self):
        """
        This function returns a dictionary from BlackFriday class input 
        """
        logging.info("Entered get_blackfriday_data_as_dict method as BlackFriday class")

        try:
            input_data = {
                "Gender" : [self.gender],
                "Age" : [self.age],
                "Occupation" : [self.occupation], 
                "City_Category" : [self.city_category],
                "Stay_In_Current_City_Years" : [self.stay_in_current_city_years], 
                "Marital_Status" : [self.marital_status], 
                "Product_Category_1" : [self.product_category_1], 
                "Product_Category_2" : [self.product_category_2], 
                "Product_Category_3" : [self.product_category_3], 

            }



            logging.info("Created blackfriday data dict")

            logging.info("Exited get_blackfriday_data_as_dict method as BlackFridayData class")

            return input_data

        except Exception as e:
            raise BlackFridayException(e, sys) from e

class BlackFridayPredictor:
    def __init__(self,prediction_pipeline_config: BlackFridayPredictorConfig = BlackFridayPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise BlackFridayException(e, sys)

    def predict(self, dataframe) -> str:
        """
        This is the method of BlackFridayPredictor
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of BlackFridayPredictor class")
            logging.info(f"user dataframe: {dataframe}")

            model = BlackFridayEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise BlackFridayException(e, sys)