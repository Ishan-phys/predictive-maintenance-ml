import requests
import json
import os

import numpy as np

from src.utils import convert_to_timestamp

def txt_to_json(data_filepath, bearing_num=1):
    """Converts the txt file to json format.

    Args:
        data_filepath (str): filepath to the data.
        bearing_num (int, optional): Defaults to 1.
    """
    data = np.loadtxt(data_filepath, delimiter='\t', dtype=float)[:,bearing_num-1]
    epoch = convert_to_timestamp(date_string=data_filepath.split('/')[-1])

    data_dict = {
            'timeStamp': int(epoch),
            'bearingNum': bearing_num,
            'accelData': data.tolist()
        }

    return data_dict


def send_requests(request_type='get', body=None):
    """Send requests to the API.

    Args:
        request_type (str, optional): type of request. Defaults to 'get'.
        body (dict_, optional): dict. Defaults to None.

    Returns:
        _type_: _description_
    """
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
        # print(response.json())

    return response


if __name__ == "__main__":

    data_dir = 'artifacts/data/raw/2nd_test'
    bearing_num = 3

    for filename in sorted(os.listdir(data_dir))[400:401]:
        print(filename)
        body = txt_to_json(data_filepath=os.path.join(data_dir, filename), bearing_num=bearing_num)
        response = send_requests(request_type='post', body=body)

        # Check the response status code
        if response.status_code == 200:
            # Success!
            print(response.json())
        else:
            # Error!
            print(response.status_code)

