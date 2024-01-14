import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

from sklearn.ensemble import IsolationForest

from src.exception import CustomException
from src.logger import logger

from src.utils import save_object, convert_prediction_to_label

@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join("artifacts", "models", "model.pkl")
    proccessed_data_filepath = os.path.join("artifacts", "data", "transformed", "processed_data.csv")
    training_data_filepath = os.path.join("artifacts", "data", "transformed", "train_data.csv")
    validation_data_filepath = os.path.join("artifacts", "data", "transformed", "val_data.csv")
    testing_data_filepath = os.path.join("artifacts", "data", "transformed", "test_data.csv")
    accepted_model_accuracy = 0.80


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def prepare_training_data(self):
        """Prepare the training data for training the ML model"""
        try:
            train_df = pd.read_csv(self.model_trainer_config.training_data_filepath)
            val_df   = pd.read_csv(self.model_trainer_config.validation_data_filepath)

            X_train = train_df.drop(columns=["timestamp"])
            X_val   = val_df.drop(columns=["timestamp"])
        
        except Exception as e:
            raise CustomException(e, sys)
        
        return X_train, X_val
        
    def evaluate_models(self, X_val, model):
        """Evaluate the ML model on the validation data

        Args:
            X_val (np array): Validation data
            model :the trained ml model

        Returns:
            float: accuracy of the model
        """
        try:
            # Get the scores on the validation data
            y_pred_val = model.predict(X_val)  
            y_pred_val = convert_prediction_to_label(y_pred_val)

            # Count the number of anomalies in the validation data
            accuracy = np.sum(y_pred_val == 0) / len(y_pred_val)

            logger.info(f"Model accuracy: {accuracy}")

        except Exception as e:
            raise CustomException(e,sys)
        
        return accuracy, y_pred_val
        
    def train_model(self, X_train, X_val, params:dict):
        """Train the ML model on the training data

        Args:
            X_train (np array): Training data
            X_val (np array): Test data
            params (dict): Hyperparameters for the model

        Returns:
            model: Trained ML model
        """
        try:
            # Instantiate the model
            model = IsolationForest(**params)
            
            # Train the model
            model.fit(X_train)

            # Get the scores on the training data
            y_pred_train = model.predict(X_train)
            y_pred_train = convert_prediction_to_label(y_pred_train)

            # Evaluate the model on the validation data
            model_accuracy, y_pred_val = self.evaluate_models(X_val, model)
            
            # Save the model if the accuracy is greater than the accepted model accuracy
            if model_accuracy < self.model_trainer_config.accepted_model_accuracy:
                raise Exception(f"Model accuracy is less than {self.model_trainer_config.accepted_model_accuracy}")
            else:
                save_object(
                    obj=model,
                    filepath=self.model_trainer_config.trained_model_filepath
                )
                logger.info(f"Model saved at {self.model_trainer_config.trained_model_filepath}")
                
        except Exception as e:
            raise CustomException(e, sys)
        
        return model, y_pred_train, y_pred_val
    
    def predict_test(self, model):
        """Predict on the test data

        Args:
            model :the trained ml model

        Returns:
            np array: predictions on the test data
        """
        try:
            df_test = pd.read_csv(self.model_trainer_config.testing_data_filepath)
            X_test = df_test.drop(columns=["timestamp"])

            y_pred_test = model.predict(X_test)
            y_pred_test = convert_prediction_to_label(y_pred_test)

            logger.info(f"Successfully predicted on the test data.")

        except Exception as e:
            raise CustomException(e, sys)
        
        return y_pred_test
    
    def save_predictions(self, data_filepath, y_preds, save_dir='artifacts/data/predictions'):
        """Save the predictions on the test data

        Args:
            data_filepath (str): Filepath to the test data
            y_test_dec (np array): predictions on the test data
            save_dir (str, optional): Directory to save the predictions. Defaults to 'artifacts/data/predictions'.
        """
        try:
            df = pd.read_csv(data_filepath)
            df["scores"] = y_preds
            df.to_csv(os.path.join(save_dir, 'predictions.csv'), index=False)

            logger.info(f"Successfully saved the predictions on the test data.")

        except Exception as e:
            raise CustomException(e, sys)