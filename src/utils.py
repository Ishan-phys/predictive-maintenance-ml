import sys 
import pickle
from datetime import datetime

from src.exception import CustomException


def convert_to_timestamp(date_string):
    """Convert the date string to a timestamp

    Args:
        date_string (str): Date string in the format of YYYY.MM.DD.HH.MM.SS. Eg. "2004.02.12.10.32.39"

    Returns:
        str: Timestamp in the format of YYYY-MM-DD HH:MM:SS. Eg. "2004-02-12 10:32:39"
    """
    # Define the format of the input string
    format_string = "%Y.%m.%d.%H.%M.%S"

    # Convert the string to a datetime object
    dt_object = datetime.strptime(date_string, format_string)

    # Convert the datetime object to a string in a desired format
    formatted_date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_date_string


def save_object(obj, filepath):
    """Save an object to a file

    Args:
        obj (object): Object to be saved
        filepath (str): Filepath to save the object to
    """
    try:
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise CustomException(e, sys)
    
    return None
    

def load_object(filepath):
    """Load an object from a file

    Args:
        filepath (str): Filepath to load the object from

    Returns:
        object: Loaded object
    """
    try:
        with open(filepath, "rb") as f:
            obj = pickle.load(f)
    except Exception as e:
        raise CustomException(e, sys)
        
    return obj


def convert_prediction_to_label(y_pred):
    """Convert the predictions to labels

    Args:
        y_pred (np array): Predictions

    Returns:
        np array: Labels
    """
    return (y_pred == -1).astype(int)