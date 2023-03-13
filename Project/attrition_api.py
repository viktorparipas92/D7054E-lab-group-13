from io import StringIO

import pandas

from kaggle_api import (
    get_file_download_url, get_from_kaggle_api, KAGGLE_API_ROOT
)


DATASET_OWNER = 'pavansubhasht'
DATASET_NAME = 'ibm-hr-analytics-attrition-dataset'

KAGGLE_DATASET_LIST_URL = (
    f"{KAGGLE_API_ROOT}datasets/list/{DATASET_OWNER}/{DATASET_NAME}"
)


def find_latest_filename(dataset_files_list):
    return dataset_files_list['datasetFiles'][-1]['name']


def fetch_data():
    attrition_dataset = get_from_kaggle_api(KAGGLE_DATASET_LIST_URL)
    latest_attrition_data_filename = find_latest_filename(attrition_dataset )
    download_url = get_file_download_url(
        DATASET_OWNER, DATASET_NAME, latest_attrition_data_filename
    )
    covid_data = get_from_kaggle_api(download_url, as_dict=False)
    covid_dataframe = pandas.read_csv(StringIO(covid_data))
    return covid_dataframe


if __name__ == '__main__':
    fetch_data()

