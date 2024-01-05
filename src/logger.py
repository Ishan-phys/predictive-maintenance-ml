import logging 
import logging.config
import yaml
import os

# Load the logging configuration
with open(os.path.join(os.getcwd(), 'src', 'configs', 'logging.yaml'), 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Create the logger
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')