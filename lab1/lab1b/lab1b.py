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


if __name__ == '__main__':
    COVID_URL = 'https://api.covid19api.com/summary'
    response_dict = get_as_dict(COVID_URL)
    for country_dict in response_dict['Countries']:
        CovidData(
            name=country_dict['Country'],
            region=...,
            total_cases=country_dict['TotalConfirmed'],
            total_deaths=country_dict['TotalDeaths'],

        )


