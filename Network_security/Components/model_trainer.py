import os
import sys
import mlflow
from Network_security.Exception.exception import NetworkSecurityException
from Network_security.Logging.logging import logging
from Network_security.Constants import training_pipeline
from Network_security.Entity.config_entity import ModelTrainerConfig
from Network_security.Entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from Network_security.Utils.ml_utils.model.estimator import NetworkModel
from Network_security.Utils.main_utils.utils import save_0bject, load_numpy_array, load_object, evaluate_models
import numpy as np
from Network_security.Utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    
)

class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config= model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


    def track_mlflow(self,best_model,classificationmetric):
            with mlflow.start_run():
                f1_score=classificationmetric.f1_score
                precision_score=classificationmetric.precision_score
                recall_score=classificationmetric.recall_score
                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision", precision_score)
                mlflow.log_metric("recall_score", recall_score)
                mlflow.sklearn.log_model(best_model, "model")
    def train_model(self,x_train, y_train, x_test, y_test):
        
        models= {
                "LogisticRegression": LogisticRegression(verbose=1),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1)
            }
            
        params={
                "LogisticRegression": {
                    
                },
                "KNeighborsClassifier": {
                    'n_neighbors': [3, 5, 7],
                    'weights': ['uniform', 'distance']
                },
                "DecisionTreeClassifier": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                   # 'max_depth': [None, 10, 20, 30],
                    #'splitter': ['best', 'random']
                },
                "RandomForestClassifier": {
                    'n_estimators': [50, 100, 200],
                   # 'criterion': ['gini', 'entropy'],
                    #'max_depth': [None, 10, 20]
                },
                "AdaBoostClassifier": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 1.0]
                },
                "GradientBoostingClassifier": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'subsample': [0.6, 0.8, 1.0]
                }
            } 
        model_report: dict = evaluate_models(x_train,y_train,x_test,y_test, models,params)
        best_model_score=max(sorted(model_report.values()))
        best_model_name= list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

       
        
        best_model= models[best_model_name]
        y_train_pred= best_model.predict(x_train)
        classification_train_metric= get_classification_score(y_true=y_train, y_pred=y_train_pred)
        self.track_mlflow(best_model,classification_train_metric)
        
        y_test_pred= best_model.predict(x_test)
        classification_test_metric= get_classification_score(y_test,y_test_pred)
        self.track_mlflow(best_model, classification_test_metric)
                                        
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path= os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        network_model= NetworkModel(preprocessor=preprocessor, model= best_model)
        save_0bject(self.model_trainer_config.trained_model_file_path, obj= NetworkModel)
    
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                    train_metrix_artifact=classification_train_metric,test_metrix_artifact=classification_test_metric)
        logging.info(f"Model trainer artifact : {model_trainer_artifact}")
        return model_trainer_artifact
            
        
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path= self.data_transformation_artifact.transformed_train_file_path
            test_file_path= self.data_transformation_artifact.transformed_test_file_path
            train_array= load_numpy_array(train_file_path)
            test_array= load_numpy_array(test_file_path)
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    