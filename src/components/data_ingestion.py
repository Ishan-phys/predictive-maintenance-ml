import os 
import sys
import urllib.request
import zipfile
from rarfile import RarFile

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logger


@dataclass
class DataIngestionConfig:
    """Data ingestion configuration

    Returns:
        obj: dataclass object
    """
    raw_data_dir: str = os.path.join('artifacts', 'data', 'raw')
    transformed_data_dir: str = os.path.join('artifacts', 'data', 'transformed')
    train_data_filepath: str = os.path.join('artifacts', 'data', 'transformed', 'train')


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def download_data(data_url: str, data_dir: str) -> None:
        """Download the data
        
        Args:
            data_url (str): URL to the data
            data_dir (str): path to the data directory
        """
        try:
            # Download the data from the URL and extract it to the raw data directory
            urllib.request.urlretrieve(data_url, data_dir)
            logger.info(f'Data download completed successfully from the URL {data_url}')

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def extract_zipfile(self, zip_filepath: str) -> None:
        """Extract the zip file
        
        Args:
            zip_filepath (str): path to the zip file
        """
        try:
            # Extract the zipped file to the raw data directory
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(self.ingestion_config.raw_data_dir)
            logger.info('Data extraction from zip file completed successfully')

            # Delete the zip file from the raw data directory
            os.remove(zip_filepath)
            
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def extract_rarfile(self, rar_filepath: str) -> None:
        """Extract the rar file
        
        Args:
            rar_filepath (str): path to the rar file
        """
        try:
            # Extract the rar file to the raw data directory
            with RarFile(rar_filepath, 'r') as rar_ref:
                rar_ref.extractall(self.ingestion_config.raw_data_dir)
            logger.info('Data extraction from rarfile completed successfully')
            
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)