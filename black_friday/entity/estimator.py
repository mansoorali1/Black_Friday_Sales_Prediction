import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from black_friday.exception import BlackFridayException
from black_friday.logger import logging
from black_friday.entity.artifact_entity import DataTransformationArtifact

# class TargetValueMapping:
#     def __init__(self):
#         self.Certified:int = 0
#         self.Denied:int = 1
#     def _asdict(self):
#         return self.__dict__
#     def reverse_mapping(self):
#         mapping_response = self._asdict()
#         return dict(zip(mapping_response.values(),mapping_response.keys()))
    



class BlackFridayModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        # self.preprocessing_object = DataTransformationArtifact.transformed_object_file_path
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data
        At last it performs prediction on transformed features
        """
        logging.info("Entered predict method of UTruckModel class")
        
        logging.info(f"preprocessing object: {self.preprocessing_object}")
        logging.info(f"trained model object : {self.trained_model_object }")

        try:
            logging.info("Using the trained model to get predictions")
            
            xx=type(dataframe)
            yy=dataframe.shape
            logging.info(f"the data frame is : {dataframe}")
            logging.info(f"the data frame type is an shape is  : {xx},{yy}")


            dataframe['Gender'] = dataframe['Gender'].astype('str')
            dataframe['Age'] = dataframe['Age'].astype('category')
            dataframe['Occupation'] = dataframe['Occupation'].astype(int)
            dataframe['City_Category'] = dataframe['City_Category'].astype('category')
            dataframe['Stay_In_Current_City_Years'] = dataframe['Stay_In_Current_City_Years'].astype('str')
            dataframe['Marital_Status'] = dataframe['Marital_Status'].astype(int)
            dataframe['Product_Category_1'] = dataframe['Product_Category_1'].astype(int)
            # dataframe['Product_Category_2'] = dataframe['Product_Category_2'].astype(int)
            # dataframe['Product_Category_3'] = dataframe['Product_Category_3'].astype(int)        
            dataframe['Stay_In_Current_City_Years'] = dataframe['Stay_In_Current_City_Years'].str.replace("+", "", regex=False)
            dataframe['Stay_In_Current_City_Years'] = dataframe['Stay_In_Current_City_Years'].astype(int)
            dataframe['Gender']=dataframe['Gender'].map({'F':0,'M':1})
            dataframe['Gender'] = dataframe['Gender'].astype(int)
            
            logging.info(f"the data frame is : {dataframe}")
            logging.info(f"data types  : {dataframe.dtypes}")
            logging.info(f"data types  : {type(dataframe)}")
            print(f"datafranme is {dataframe}")
            print(f"datafranme null values {dataframe.isna().sum()}")
            print(f"preprocessing object {self.preprocessing_object}")

            transformed_feature = self.preprocessing_object.transform(dataframe)
            
            logging.info(f"trasformed feature is : {transformed_feature}")

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)  
            # return self.trained_model_object.predict(dataframe)  


        except Exception as e:
            raise BlackFridayException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"