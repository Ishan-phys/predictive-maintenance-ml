import os
import sys
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

from datetime import datetime, timedelta

from src.logger import logger
from src.exception import CustomException

load_dotenv()

def database_connection(local=True):
    """Connect to the MongoDB database
    
    local (bool): whether to connect to the local database or the cloud database
    """
    if local:
        client = MongoClient("localhost", 27017)
    else:
        # Get the database URI from the environment variables
        database_uri = os.getenv("DATABASE_URL")

        # Create a new client and connect to the server
        client = MongoClient(database_uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(f"Could not connect to MongoDB: {error_message}")
    
    return client


def insert_data(db_name, collection_name, data, local=True):
    """Insert data into the MongoDB database
    
    Args:
        db (MongoClient): the database connection
        collection_name (str): the name of the collection
        data (dict): the data to insert
    """
    try:
        client = database_connection(local)

        # Access a specific database
        db = client[db_name]

        # Access a specific collection (i.e Table)
        collection = db[collection_name]

        # Insert the data into the collection
        collection.insert_one(data)
        logger.info(f"Successfully inserted data into the {collection_name} collection")

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(f"Could not insert data into the {collection_name} collection: {error_message}")

    return None


def fetch_data_db(db_name, collection_name, date_string, bearing_num, local=True): 
    """Fetch data from the MongoDB database
    
    Args:
        db (MongoClient): the database connection
        collection_name (str): the name of the collection

    Returns:
        item_details (dict): the data from the collection
    """
    data_list = []

    client = database_connection(local=local)

    # Access a specific database
    db = client[db_name]

    # Access a specific collection (i.e Table)
    collection = db[collection_name]

    if date_string.lower() == 'all':
        # Query with conditions
        query = {
            'bN': int(bearing_num)
        }

    else:
        # Convert input date string to timestamp
        input_date = datetime.strptime(date_string, '%d-%b-%Y')
        timestamp = int(input_date.timestamp())

        # Query with conditions
        query = {
            'tS': {'$gte': timestamp, '$lt': timestamp + 86400},
            'bN': int(bearing_num)
        }

    item_details = collection.find(query)

    for item in item_details:
        # This does not give a very readable output
        data_list.append(item)

    return data_list



if __name__ == "__main__":

    import pandas as pd
    db_name = "machinehealth"
    collection_name = "test"
    date_string = '17-Feb-2004'
    bearing_num = 1
    local = False

    data_list = fetch_data_db(db_name, collection_name, date_string, bearing_num, local=local)

    df = pd.DataFrame(data_list)

    print(df)