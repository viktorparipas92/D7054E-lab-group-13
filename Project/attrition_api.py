from io import StringIO

import pandas as pd

from kaggle_api import get_file_download_url, KAGGLE_API_ROOT, KaggleAPI


DATASET_OWNER = 'pavansubhasht'
DATASET_NAME = 'ibm-hr-analytics-attrition-dataset'

KAGGLE_DATASET_LIST_URL = (
    f"{KAGGLE_API_ROOT}datasets/list/{DATASET_OWNER}/{DATASET_NAME}"
)


def fetch_data() -> pd.DataFrame:
    kaggle_api = KaggleAPI()
    attrition_dataset_list_response: dict = kaggle_api.get(
        KAGGLE_DATASET_LIST_URL
    )
    attrition_dataset_filename = attrition_dataset_list_response[
        'datasetFiles'
    ][0]['name']
    download_url = get_file_download_url(
        DATASET_OWNER, DATASET_NAME, attrition_dataset_filename
    )
    attrition_data: str = kaggle_api.get(download_url, as_dict=False)
    attrition_dataset: pd.DataFrame = pd.read_csv(StringIO(attrition_data))
    return attrition_dataset
