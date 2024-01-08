import sys
from src.logger import logger

def error_message_details(error, error_detail:sys):
    """Error message details

    Args:
        error (obj): exception object 
        error_detail (sys): sys object

    Returns:
        str: error message
    """
    _, _, exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f'{error} in {filename} at line {line_number}'

    return error_message

class CustomException(Exception):
    
    def __init__(self, error, error_detail:sys):
        """Custom exception

        Args:
            error (obj): exception object 
            error_detail (sys): sys object
        """
        super().__init__(error)
        self.error_message = error_message_details(error, error_detail)

    def __str__(self):
        """String representation of the exception

        Returns:
            str: error message
        """
        return self.error_message