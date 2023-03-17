import json
from io import StringIO
from typing import Union, Dict, Optional

import pandas as pd
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
        self.root = root

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


class KaggleDataset:
    def __init__(self, api: KaggleAPI, owner: str, name: str):
        self._api = api
        self.dataset_list_url = f"{self._api.root}datasets/list/{owner}/{name}"
        self._owner = owner
        self._name = name
        self._datasets = {}

    def fetch_datasets(self) -> dict:
        datasets = self._api.get(self.dataset_list_url)
        self._datasets = datasets
        return self._datasets

    def download(self, filename: str) -> pd.DataFrame:
        download_url = self._build_file_download_url(filename)
        data: str = self._api.get(download_url, as_dict=False)
        dataset: pd.DataFrame = pd.read_csv(StringIO(data))
        return dataset

    def _build_file_download_url(self, filename):
        return (
            f"{self._api.root}datasets/download/"
            f"{self._owner}/{self._name}/{filename}"
        )
