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

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_VALID_DIR : str = "valid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME= "preprocessing.pkl"

SCHEMA_FILE_PATH=os.path.join('data_schema', 'schema.yaml')

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR :  str= "transformed_object"
DATA_TRANSFORMATION_IMPUTE_PARAMS: dict= {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TERST_FILE_PATH : str = "test.npy"