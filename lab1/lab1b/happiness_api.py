from io import StringIO

import pandas

from kaggle_api import (
    get_file_download_url, get_from_kaggle_api, KAGGLE_API_ROOT
)


DATASET_OWNER = 'mathurinache'
DATASET_NAME = 'world-happiness-report'

KAGGLE_DATASET_LIST_URL = (
    f"{KAGGLE_API_ROOT}datasets/list/{DATASET_OWNER}/{DATASET_NAME}"
)


def find_filename_for_year(dataset_files_list, year):
    for dataset_file in dataset_files_list['datasetFiles']:
        if str(year) in dataset_file['name']:
            return dataset_file['name']

    return None


if __name__ == '__main__':
    happiness_dataset = get_from_kaggle_api(KAGGLE_DATASET_LIST_URL)
    filename_2019 = find_filename_for_year(happiness_dataset, 2019)
    download_url_2019 = get_file_download_url(
        DATASET_OWNER, DATASET_NAME, filename_2019)
    happiness_2019_data = get_from_kaggle_api(download_url_2019, as_dict=False)
    happiness_2019_dataframe = pandas.read_csv(StringIO(happiness_2019_data))
    print(happiness_2019_dataframe)

