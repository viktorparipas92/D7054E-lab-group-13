from io import StringIO

import pandas
import pandas as pd

from kaggle_api import (
    get_file_download_url, get_from_kaggle_api, KAGGLE_API_ROOT
)


DATASET_OWNER = 'pavansubhasht'
DATASET_NAME = 'ibm-hr-analytics-attrition-dataset'

KAGGLE_DATASET_LIST_URL = (
    f"{KAGGLE_API_ROOT}datasets/list/{DATASET_OWNER}/{DATASET_NAME}"
)


def find_latest_filename(dataset_list_response: dict) -> str:
    return dataset_list_response['datasetFiles'][-1]['name']


def fetch_data() -> pd.DataFrame:
    attrition_dataset_list_response: dict = get_from_kaggle_api(
        KAGGLE_DATASET_LIST_URL
    )
    latest_attrition_data_filename = find_latest_filename(
        attrition_dataset_list_response
    )
    download_url = get_file_download_url(
        DATASET_OWNER, DATASET_NAME, latest_attrition_data_filename
    )
    attrition_data: str = get_from_kaggle_api(download_url, as_dict=False)
    attrition_dataset: pd.DataFrame = pandas.read_csv(StringIO(attrition_data))
    return attrition_dataset


if __name__ == '__main__':
    fetch_data()
