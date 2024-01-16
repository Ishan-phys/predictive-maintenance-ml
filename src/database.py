import os
import sys
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

from datetime import datetime

from src.logger import logger
from src.exception import CustomException

load_dotenv()

def database_connection():
    """Connect to the MongoDB database"""

    # Get the database URI from the environment variables
    database_uri = os.getenv("DATABASE_URL")

    # Get the database name from the environment variables
    database_name = os.getenv("DATABASE_NAME")

    # Create a new client and connect to the server
    client = MongoClient(database_uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(f"Could not connect to MongoDB: {error_message}")
    
    return client[database_name]


def insert_data(db, collection_name, data):
    """Insert data into the MongoDB database
    
    Args:
        db (MongoClient): the database connection
        collection_name (str): the name of the collection
        data (dict): the data to insert
    """
    try:
        collection = db[collection_name]

        # Insert the data into the collection
        collection.insert_one(data)
        logger.info(f"Successfully inserted data into the {collection_name} collection")
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(f"Could not insert data into the {collection_name} collection: {error_message}")

    return None


if __name__ == "__main__":

    # Get the database connection
    db = database_connection()

    now = datetime.now()

    id = now.strftime("%d%m%Y%H%M%S")
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

    print(now)

    # Fetch the data 
    response_data = {
            "_id": str(id),
            "timeStamp": timestamp,
            "rmsAccel":float(0.345),
            "prediction": int(0)
        }
    
    # Insert the data into the database
    insert_data(db, "test", response_data)