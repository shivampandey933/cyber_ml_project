import os
import sys
from Network_security.Exception.exception import NetworkSecurityException
from Network_security.Logging.logging import logging
from Network_security.Constants import training_pipeline
from Network_security.Entity.config_entity import DataTransformationConfig
from Network_security.Entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
import numpy as np
import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from Network_security.Constants.training_pipeline import TARGET_COLUMN
from Network_security.Constants.training_pipeline import DATA_TRANSFORMATION_IMPUTE_PARAMS
from Network_security.Utils.main_utils.utils import save_numpy_array_data, save_0bject

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
         try:
                self.data_validation_artifact= data_validation_artifact
                self.data_transformation_config= data_transformation_config
         except Exception as e:
              raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
         try:
              return pd.read_csv(file_path)
         except Exception as e:
            raise NetworkSecurityException(e,sys)  

    def get_data_transformer_object(cls)-> Pipeline:
         logging.info("Entered the get_data_transformer_object method of Data Transformation class")   
         try:
           imputer: KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)
           logging.info(f"initialise KNNImputer with params: {DATA_TRANSFORMATION_IMPUTE_PARAMS}")
           processor: Pipeline=Pipeline([("imputer", imputer)])
           return processor
         except Exception as e:
              raise NetworkSecurityException(e,sys)     

    def initiate_data_transformation(self)->DataTransformationArtifact:
         logging.info("starting data transformation")
         try:
            logging.info("starting data transformation")
            train_df= DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df= DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_feature_train_df= train_df.drop(columns=[TARGET_COLUMN], axis=1)
            input_feature_test_df= test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df= train_df[TARGET_COLUMN]
            target_feature_train_df= target_feature_train_df.replace(-1,0)
            target_feature_test_df= test_df[TARGET_COLUMN]
            target_feature_test_df= target_feature_test_df.replace(-1,0)
            preprocessor_object= self.get_data_transformer_object().fit(input_feature_train_df)
            transformed_input_train_feature= preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature= preprocessor_object.transform(input_feature_test_df)
            train_arr= np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr= np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_data_test_file_path, test_arr)
            save_0bject(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            data_transformation_artifact= DataTransformationArtifact(
                 transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                 transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                 transformed_test_file_path=self.data_transformation_config.transformed_data_test_file_path
            )
            return data_transformation_artifact

         except Exception as e:
              raise NetworkSecurityException(e,sys)
