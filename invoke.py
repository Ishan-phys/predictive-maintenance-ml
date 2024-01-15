import requests
import json

import numpy as np

from src.utils import convert_to_timestamp

def txt_to_json(data_filepath, bearing_num=1):
    """_summay_

    Args:
        data_filepath (_type_): _description_
        bearing_num (int, optional): _description_. Defaults to 1.
    """
    data = np.loadtxt(data_filepath, delimiter='\t', dtype=float)[:,bearing_num-1]
    timestamp = convert_to_timestamp(date_string=data_filepath.split('/')[-1])

    data_dict = {
        'accelData': data.tolist(),
        'timeStamp': timestamp
    }

    return data_dict


def send_requests(request_type='get', body=None):

    if request_type == 'get':
        url = "http://localhost:8080/ping"

        response = requests.get(url)

        print(response.json())

    elif request_type == 'post':
        url = "http://localhost:8080/invocations"

        # Define the headers
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))

        print(response.json())

    return response




if __name__ == "__main__":

    body = txt_to_json(data_filepath="artifacts/data/raw/2nd_test/2004.02.12.21.32.39", bearing_num=1)

    response = send_requests(request_type='post', body=body)

    # Check the response status code
    if response.status_code == 200:
        # Success!
        print(response.json())
    else:
        # Error!
        print(response.status_code)

