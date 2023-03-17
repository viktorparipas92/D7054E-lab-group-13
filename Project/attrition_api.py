import pandas as pd

from kaggle_api import KaggleAPI, KaggleDataset

DATASET_OWNER = 'pavansubhasht'
DATASET_NAME = 'ibm-hr-analytics-attrition-dataset'


class AttritionDataset(KaggleDataset):
    @staticmethod
    def get_filename(dataset_list_response: dict) -> str:
        return dataset_list_response['datasetFiles'][0]['name']


def fetch_data() -> pd.DataFrame:
    kaggle_api = KaggleAPI()
    attrition_dataset = AttritionDataset(
        kaggle_api, owner=DATASET_OWNER, name=DATASET_NAME
    )

    attrition_datasets: dict = attrition_dataset.fetch_datasets()
    filename = attrition_dataset.get_filename(attrition_datasets)
    attrition_dataframe = attrition_dataset.download(filename)
    return attrition_dataframe
