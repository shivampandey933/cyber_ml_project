from Network_security.Components.data_ingestion import DataIngestion
from Network_security.Exception.exception import NetworkSecurityException
from Network_security.Logging.logging import logging
from Network_security.Entity.config_entity import DataIngestionConfig
from Network_security.Entity.config_entity import TrainingPipelineConfig
from Network_security.Components.data_validation import DataValidation
from Network_security.Entity.config_entity import DataValidationConfig
from Network_security.Components.data_transformation import DataTransformation
from Network_security.Entity.config_entity import DataTransformationConfig
import sys
if __name__== '__main__':
    try:
        trainingpipelineconfig= TrainingPipelineConfig()
        dataingestionconfig= DataIngestionConfig(trainingpipelineconfig)
        data_ingestion= DataIngestion(dataingestionconfig)
        logging.info("Starting data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)
        data_validation_config= DataValidationConfig(trainingpipelineconfig)
        data_validation=  DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Starting data validation")
        data_validation_artifact= data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("data transformation started")
        data_transformation= DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data transformation completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)