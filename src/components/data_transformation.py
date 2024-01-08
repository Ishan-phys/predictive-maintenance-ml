import os 
import sys
import numpy as np

from dataclasses import dataclass

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
    # file_name: str
    # file_type: str
    file_delimiter: str = '\t'
    # file_header: bool
    # file_encoding: str


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
            data = np.loadtxt(data_filepath, delimiter='\t', dtype=float)
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

        

if __name__ == "__main__":
    dt = DataTransformation()

    dt.extract_data_file("artifacts/data/raw/2nd_test/2004.02.12.10.32.39")   