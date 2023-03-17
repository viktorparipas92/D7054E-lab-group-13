import json
from typing import Union, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth


KAGGLE_API_ROOT = 'https://www.kaggle.com/api/v1/'
KAGGLE_USERNAME = 'viktorparipas'
KAGGLE_API_TOKEN = '7669a17cf215d73573d5e99c9b5334ae'


class KaggleAPI:
    def __init__(
        self,
        root: str = KAGGLE_API_ROOT,
        username: Optional[str] = KAGGLE_USERNAME,
        api_token: Optional[str] = KAGGLE_API_TOKEN
    ):
        self._username = username
        self._api_token = api_token
        self._root = root

    def get(self, url, as_dict=True) -> Union[Dict, str]:
        response = self._get(url)
        if as_dict:
            return json.loads(response.text)
        else:
            return response.text

    def _get(self, url):
        if self._username is not None and self._api_token is not None:
            basic = HTTPBasicAuth(self._username, self._api_token)
            response = requests.get(url, auth=basic)
        else:
            response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Not OK request')
        else:
            return response


def get_file_download_url(dataset_owner, dataset_name, filename):
    return (
        f"{KAGGLE_API_ROOT}datasets/download/"
        f"{dataset_owner}/{dataset_name}/{filename}"
    )
