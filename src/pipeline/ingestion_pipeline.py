import os
from src.components.data_ingestion import DataIngestion

if __name__ == "__main__":

    ingest_pip = DataIngestion()    
    ingest_pip.download_data('https://data.nasa.gov/download/brfb-gzcv/application%2Fzip', os.path.join(os.getcwd(), 'artifacts', 'data', 'raw', 'IMS.zip'))
    ingest_pip.extract_zipfile(zip_filepath='artifacts/data/raw/IMS.zip')
    ingest_pip.extract_rarfile(rar_filepath='artifacts/data/raw/IMS/1st_test.rar')
    ingest_pip.extract_rarfile(rar_filepath='artifacts/data/raw/IMS/2nd_test.rar')