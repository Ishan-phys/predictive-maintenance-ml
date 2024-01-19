import sys
import os
import numpy as np

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logger
from src.database import database_connection, insert_data
from src.utils import load_object, convert_prediction_to_label
from src.components.data_transformation import DataTransformation

# The FastAPI app for serving predictions
app = FastAPI(title="PredictionServiceApp", description="Predictor App for Vibration Data", version="0.0.1")

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*",
    "http://127.0.0.1:8089/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@dataclass
class PredictorConfig:
    """Data ingestion configuration

    Returns:
        obj: dataclass object
    """
    model_dir: str = os.path.join("opt", "program")
    sampling_rate: int = 20480


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.
class Predictor:

    def __init__(self, bearing_num):

        self.predictor_configs = PredictorConfig()
        self.model = None
        self.bearing_num = bearing_num
        
    def _load_model(self):
        """Get the model object for this instance, loading it if it's not already loaded.

        Returns:
            the model
        """
        try:
            model_file_path = os.path.join(f"model_b{self.bearing_num}.pkl")
            model = load_object(model_file_path)
            logger.info(f"Model loaded successfully from {model_file_path}.")
        
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return model

    def _predict(self, input):
        """For the input, do the predictions and return them.

        Args:
            input (np array)

        Returns:
            tuple: the prediction and the probability
        """
        try: 
            # Load the classifier and the scaler for the specified fault
            clf = self._load_model()

            n_features = input.shape[-1]
            logger.info(f"Number of features: {n_features}")

            # Get the prediction of the model on the input data
            y_pred = clf.predict(input)

            # Convert -1 to 1 (Label 1 denotes faulty file)
            y_pred = convert_prediction_to_label(y_pred)[0]
            logger.info(f'Prediction successful on the {y_pred}')
        
        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return y_pred

    def predict_faulty_or_healthy(self, data):
        """Predict if a given file is healthy or not

        Args:
            data(dictionary): the json file
            fault_type (str): the type of the fault

        Returns:
            dict: health report
        """        
        try:
            # Get the sampling rate of the data
            sampling_rate = self.predictor_configs.sampling_rate

            # Extract the features from the data
            data_transform = DataTransformation(bearing_num=self.bearing_num)

            # Get the features from the data
            features_dict = data_transform.featurize(data, sampling_rate)
            features = np.array(list(features_dict.values())).reshape(1, -1)

            # Give the prediction on the feature set (prediction = 0 or 1) and obtain the decision score
            y_pred = self._predict(input=features)

        except Exception as e:
            error_message = CustomException(e, sys)
            logger.error(error_message)

        return y_pred, features_dict


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    # Log the error here
    logger.error(f"Unhandled Exception: {exc} for request")

    method       = request.method
    url          = request.url
    headers      = request.headers
    query_params = request.query_params
    client       = request.client

    # Construct a response with the extracted information
    response_data = {
        "method": method,
        "url": url,
        "headers": dict(headers),
        "query_params": dict(query_params),
        "client": client,
    }

    return JSONResponse(content=response_data, status_code=500)


@app.get('/ping')
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""

    # status = 200 if model_health else 404
    status = 200

    return {"status": status}


@app.post("/invocations", status_code=200)
async def transformation(request: Request):
    """Prediction on a single JSON file"""

    try: 
        # Read the json data passed as the request
        post_data  = await request.json()
        logger.info(f"Request keys: {post_data.keys()}")

        # Extract the data from the request
        accel_data  = np.array(post_data.get('accelData'))
        timestamp   = post_data.get('timeStamp')
        bearing_num = post_data.get('bearingNum')

        # Instantiate the predictor class
        predictor = Predictor(bearing_num=bearing_num)

        # Get the prediction of the model on the input data
        y_pred, features_dict = predictor.predict_faulty_or_healthy(accel_data)
        logger.info(f'ML prediction on the file: {y_pred}')

        unique_id = f"{timestamp}b{bearing_num}"

        # Construct the response
        response_data = {
            "_id": unique_id,                                 # ID
            "tS"  : int(timestamp),                           # Epoch time
            "bN": int(bearing_num),                           # Bearing number
            "rA": float(round(features_dict['trms'], 3)),     # RMS acceleration
            "hS": int(y_pred)                                 # Health Status
        }

        # Insert the data into the database
        insert_data(db_name='machinehealth', collection_name='test', data=response_data, local=False)

    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)
        
    return JSONResponse(content=response_data, status_code=200)


