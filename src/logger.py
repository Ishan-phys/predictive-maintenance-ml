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