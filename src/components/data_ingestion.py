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
    raw_data_dir: str = os.path.join(os.getcwd(), 'artifacts', 'data', 'raw')
    transformed_data_dir: str = os.path.join(os.getcwd(), 'artifacts', 'data', 'transformed')
    train_data_filepath: str = os.path.join(os.getcwd(), 'artifacts', 'data', 'transformed', 'train')
    # file_name: str
    # file_type: str
    # file_delimiter: str
    # file_header: bool
    # file_encoding: str


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()


    def download_data(data_url: str, data_dir: str) -> None:
        """Download the data"""
        try:
            # Download the data from the URL and extract it to the raw data directory
            urllib.request.urlretrieve(data_url, data_dir)

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

    def extract_zipfile(self, zip_filepath: str) -> None:
        """Extract the zip file"""
        try:
            # Extract the zipped file to the raw data directory
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(self.ingestion_config.raw_data_dir)
            
            logger.info('Data extraction completed successfully')

            # Delete the zip file from the raw data directory
            os.remove(zip_filepath)
            
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)


    def extract_rarfile(self, rar_filepath: str) -> None:
        """Extract the rar file"""
        try:
            # Extract the rar file to the raw data directory
            with RarFile(rar_filepath, 'r') as rar_ref:
                rar_ref.extract(self.ingestion_config.raw_data_dir)
            
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)


if __name__ == "__main__":

    #DataIngestion.download_data('https://data.nasa.gov/download/brfb-gzcv/application%2Fzip', os.path.join(os.getcwd(), 'artifacts', 'data', 'raw', 'IMS.zip'))

    ingest_pip = DataIngestion()
    
    ingest_pip.download_data('https://data.nasa.gov/download/brfb-gzcv/application%2Fzip', os.path.join(os.getcwd(), 'artifacts', 'data', 'raw', 'IMS.zip'))
    ingest_pip.extract_zipfile(zip_filepath='artifacts/data/raw/IMS.zip')
    ingest_pip.extract_rarfile(rar_filepath='artifacts/data/raw/IMS/1st_test.rar')












if __name__ == '__main__':
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')