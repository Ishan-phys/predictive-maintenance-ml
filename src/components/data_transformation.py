import os 
import sys
import numpy as np
import pandas as pd

from dataclasses import dataclass

from src.utils import convert_to_timestamp
from src.components.features import calc_fft, calc_spectrum_features, calc_time_features
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
    file_delimiter: str = '\t'


class DataTransformation:
    def __init__(self) -> None:
        self.ingestion_config = DataTransformationConfig()

    def extract_data_file(self, data_filepath, bearing_num):
        """Extract the data from the individual plain/txt files

        Args:
            data_filepath (str): Path to the data file

        Returns:
            np array
        """
        try:
            # Extract the data from the individual files
            data = np.loadtxt(data_filepath, delimiter=self.ingestion_config.file_delimiter, dtype=float)[:,bearing_num-1]
            logger.info(f'Data extraction from file {data_filepath} completed successfully. Data Shape: {data.shape}')
            
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return data

    def featurize(self, data, sampling_rate):
        """Calculate the features from the data

        Args:
            data (np array): data

        Returns:
            np array: calculated features
        """
        try:
            features = dict()

            # Calculate the features from the data
            centered_data, fft_amplitudes, _ = calc_fft(data, sampling_rate)

            # Calculate the spectrum features
            spectrum_features = calc_spectrum_features(fft_amplitudes)
            features.update(spectrum_features)
            logger.info(f'Spectrum features calculated successfully.')

            # Calculate the time domain features
            time_features     = calc_time_features(centered_data)
            features.update(time_features)
            logger.info(f'Time domain features calculated successfully.')

            logger.info(f'Feature calculated successfully. Num features: {len(features)}')

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return features

    def featurize_all(self, data_dir, sampling_rate, bearing_num):
        """Calculate the features from the data

        Args:
            raw_files_dir (str): Path to the raw data directory
            sampling_rate (int): Sampling rate of the data
            num_files (int): Number of files to process

        Returns:
            np array: calculated features
        """
        try:    
            features_list = []

            # Loop over all the data files and obtain the features for each
            for file_name in sorted(os.listdir(data_dir)):

                # Initialize the features dictionary
                features = dict()

                # Obtain the path to the data file
                file_path = os.path.join(data_dir, file_name)
                logger.info(f'Processing file: {file_path}')

                # Obtain the timestamp of the data file
                timestamp = convert_to_timestamp(date_string=file_path.split('/')[-1])
                features.update({'timestamp':timestamp})

                # Extract the data from the individual files
                data = self.extract_data_file(file_path, bearing_num)

                # Calculate the features from the data
                calc_features = self.featurize(data, sampling_rate)
                features.update(calc_features)

                logger.info(f'Feature calculation completed successfully. Num features: {features}')

                # Append the calculate features to a list
                features_list.append(features)

                # Append the timestamp to the features
                logger.info('Feature calculation completed successfully.')

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return features_list

    def transform_to_df(self, features_list, save=False):
        """Transform the data to a pandas dataframe

        Args:
            data_arr (np array): data

        Returns:
            pandas dataframe
        """
        try:
            # Transform the data to a pandas dataframe
            df = pd.DataFrame(features_list)
            logger.info(f'Dataframe transformation completed successfully. Dataframe Shape: {df.shape}')

            if save:
                # Save the dataframe to a csv file
                df.to_csv(os.path.join(self.ingestion_config.transformed_data_dir, 'processed_data.csv'), index=False)
                logger.info(f'Dataframe saved successfully at {self.ingestion_config.transformed_data_dir}')

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return df

    def split_data(self, df, train_size=400, save=False):
        """Split the data into train and test sets

        Args:
            df (pandas dataframe): dataframe

        Returns:
            pandas dataframe, pandas dataframe: train and test sets
        """
        try:
            # Split the data into train, validation and test sets
            val_size = int(0.1 * train_size)
            train_df = df[:(train_size - val_size)]
            val_df   = df[(train_size - val_size):train_size]
            test_df  = df[train_size:]

            logger.info(f'Data split completed successfully. Train Data Shape: {train_df.shape},\nValidatation Data Shape: {val_df.shape},\nTest Data Shape: {test_df.shape}')

            if save:
                # Save the train, validation and test sets to csv files
                train_df.to_csv(os.path.join(self.ingestion_config.transformed_data_dir, 'train_data.csv'), index=False)
                val_df.to_csv(os.path.join(self.ingestion_config.transformed_data_dir, 'val_data.csv'), index=False)
                test_df.to_csv(os.path.join(self.ingestion_config.transformed_data_dir, 'test_data.csv'), index=False)
                logger.info(f'Train, validation and test sets saved successfully at {self.ingestion_config.transformed_data_dir}')

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)
        
        return None        