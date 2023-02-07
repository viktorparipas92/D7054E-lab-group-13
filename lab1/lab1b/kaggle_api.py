from lab1b import get_as_dict, get_raw_text


KAGGLE_API_ROOT = "https://www.kaggle.com/api/v1/"

KAGGLE_USERNAME = 'viktorparipas'
KAGGLE_API_TOKEN = '7669a17cf215d73573d5e99c9b5334ae'


def get_from_kaggle_api(url, as_dict=True):
    kwargs = dict(user=KAGGLE_USERNAME, password=KAGGLE_API_TOKEN)
    if as_dict:
        return get_as_dict(url, **kwargs)
    else:
        return get_raw_text(url, **kwargs)


def get_file_download_url(dataset_owner, dataset_name, filename):
    return (
        f"{KAGGLE_API_ROOT}datasets/download/"
        f"{dataset_owner}/{dataset_name}/{filename}"
    )
