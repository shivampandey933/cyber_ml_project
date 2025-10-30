from Network_security.Exception.exception import NetworkSecurityException
from Network_security.Logging.logging import logging
from Network_security.Entity.config_entity import DataIngestionConfig
from Network_security.Entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL= os.getenv("Mongo_DB_uri")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config= data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
      
    def export_collection_as_dataframe(self):
        try:
           database_name: str = self.data_ingestion_config.database_name
           collection_name: str = self.data_ingestion_config.collection_name
           self.mongo_client: pymongo.MongoClient = pymongo.MongoClient(MONGO_DB_URL)
           collection: pymongo.collection.Collection = self.mongo_client[database_name][collection_name]
           df: pd.DataFrame = pd.DataFrame(list(collection.find()))
           if "_id" in df.columns.to_list():
               df= df.drop(columns=["_id"], axis=1)
           df.replace({'na':np.nan},inplace=True)   
           return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path= self.data_ingestion_config.feature_store_file_path
            dir_path= os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set= train_test_split(dataframe, test_size= self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split")
            logging.info("exited the split_data_as_train_test method of Data Ingestion class")
            dir_path= os.path.dirname(self.data_ingestion_config.training_file_path)
            dir_path=os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False,header=True)
            logging.info("exported train and test file path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)   
    def initiate_data_ingestion(self):
        try:
            dataframe= self.export_collection_as_dataframe()
            dataframe= self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact= DataIngestionArtifact(train_file_path= self.data_ingestion_config.training_file_path,
                                                           test_file_path= self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)      
