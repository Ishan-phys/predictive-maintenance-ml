import os 
import sys
import numpy as np
import pandas as pd

from dataclasses import dataclass

from src.utils import convert_to_timestamp
from src.exception import CustomException
from src.logger import logger


@dataclass
class DataTransformationConfig:
    """Data ingestion configuration

    Returns:
        obj: dataclass object
    """
    raw_data_dir: str = os.path.join('artifacts', 'data', 'raw')
    transformed_data_dir: str = os.path.join('artifacts', 'data', 'transformed')
    train_data_filepath: str = os.path.join('artifacts', 'data', 'transformed', 'train')
    file_delimiter: str = '\t'


class DataTransformation:
    def __init__(self) -> None:
        self.ingestion_config = DataTransformationConfig()

    def extract_data_file(self, data_filepath):
        """Extract the data from the individual plain/txt files

        Args:
            data_filepath (str): Path to the data file

        Returns:
            np array
        """
        try:
            # Extract the data from the individual files
            data = np.loadtxt(data_filepath, delimiter=self.ingestion_config.file_delimiter, dtype=float)
            logger.info(f'Data extraction from file {data_filepath} completed successfully. Data Shape: {data.shape}')
            
            return data

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def featurize(self, data):
        """Calculate the features from the data

        Args:
            data (np array): data

        Returns:
            np array: calculated features
        """
        try:
            # Calculate the features from the data
            features = np.mean(data, axis=1)
            logger.info(f'Feature calculation completed successfully. Features Shape: {features.shape}')

            return features

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)


    def featurize_all(self, raw_files_dir, num_files):
        """Calculate the features from the data

        Args:
            data_arr (np array): data

        Returns:
            np array: calculated features
        """
        try:    
            features = []

            # Loop over all the data files and obtain the features for each
            for file_path in os.listdir(raw_files_dir)[:int(num_files)]:

                # Extract the data from the individual files
                data = self.extract_data_file(file_path)

                # Calculate the features from the data
                features = self.featurize(data)

                # Obtain the timestamp of the data file
                timestamp = convert_to_timestamp(date_string=file_path.split('/')[-1])

                # Append the timestamp to the features
                logger.info(f'Feature calculation completed successfully. Features Shape: {features.shape}')

            return features

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def transform_to_df(self, data_arr):
        """Transform the data to a pandas dataframe

        Args:
            data_arr (np array): data

        Returns:
            pandas dataframe
        """
        try:
            # Transform the data to a pandas dataframe
            df = pd.DataFrame(data_arr)
            logger.info(f'Dataframe transformation completed successfully. Dataframe Shape: {df.shape}')

            return df

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def split_data(self, df, train_size=0.8, val_size=0.2):
        """Split the data into train and test sets

        Args:
            df (pandas dataframe): dataframe

        Returns:
            pandas dataframe, pandas dataframe: train and test sets
        """
        try:
            # Split the data into train and test sets
            train_df = df.sample(frac=0.8, random_state=0)
            test_df  = df.drop(train_df.index)
            logger.info(f'Data split completed successfully. Train Data Shape: {train_df.shape}, Test Data Shape: {test_df.shape}')

            return train_df, test_df

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        

if __name__ == "__main__":
    dt = DataTransformation()

    dt.extract_data_file("artifacts/data/raw/2nd_test/2004.02.12.10.32.39")   