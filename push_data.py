import sys, os, json
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("Mongo_DB_uri")
import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo
from Network_security.Exception.exception import NetworkSecurityException
from Network_security.Logging.logging import logging
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
             raise NetworkSecurityException(e,sys)
    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
                raise NetworkSecurityException(e,sys)    
    def insert_data_mongoDb(self,records,database,collection):
         try:
              self.records=records
              self.database=database
              self.collection=collection
              self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
              self.mongo_client= self.mongo_client[self.database]  
              self.collection=self.mongo_client[self.collection]    
              self.collection.insert_many(self.records)
              return len(self.records)                                
                                                    
         except Exception as e:
              raise NetworkSecurityException(e,sys)   

if __name__=='__main__':
     try:
          File_path="Network_Data\phisingData.csv"
          DATABASE="Shivam_Pandey_db"
          collection="Network_security_collection"
          network_obj=NetworkDataExtract()
          records=network_obj.csv_to_json(File_path)
          print(records)
          no_of_records=network_obj.insert_data_mongoDb(records,DATABASE,collection)
          print(no_of_records)
     except Exception as e:
          raise NetworkSecurityException(e,sys)
