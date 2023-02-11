import requests
from requests.auth import HTTPBasicAuth
import json


def get(url, user=None, password=None):
    if user is not None and password is not None:
        basic = HTTPBasicAuth(user, password)
        response = requests.get(url, auth=basic)
    else:
        response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Not OK request")
    else:
        return response


def get_as_dict(url, user=None, password=None):
    response = get(url, user, password)
    return json.loads(response.text)


def get_raw_text(url, user=None, password=None):
    response = get(url, user, password)
    return response.text
