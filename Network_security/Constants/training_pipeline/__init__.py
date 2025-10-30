import os,sys
import numpy as np
import pandas as pd
DATA_INGESTION_COLLECTION_NAME: str= "Network_security_collection"
DATA_INGESTION_DATABASE_NAME: str = "Shivam_Pandey_db"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2


TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "Network_security"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phisingData.csv"
TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME: str = "test.csv"