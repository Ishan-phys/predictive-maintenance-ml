import os 
import sys 
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