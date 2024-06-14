from black_friday.data_access.blackfriday_data import BlackFridayData
from black_friday.entity.config_entity import DataIngestionConfig

data_ingestion_config=DataIngestionConfig()
 
data_ingestion_config = data_ingestion_config

usvisa_data = BlackFridayData()
dataframe = usvisa_data.export_collection_as_dataframe(collection_name=
                                                        data_ingestion_config.collection_name)


print(dataframe)
