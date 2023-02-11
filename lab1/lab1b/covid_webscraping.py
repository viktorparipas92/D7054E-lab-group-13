from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


WHO_COVID_DATA_URL = 'https://covid19.who.int/table'


def scrape():
    driver, page_source = get_page_source()

    soup = BeautifulSoup(page_source, features='html.parser')
    column_names = get_column_names(soup)
    covid_data = pd.DataFrame(columns=column_names)

    column_totals = get_column_totals(soup)
    covid_data.loc[len(covid_data.index)] = column_totals

    country_rows = get_country_rows(soup)
    for row in country_rows:
        values = get_row_values(row)
        covid_data.loc[len(covid_data.index)] = values

    return covid_data


def get_row_values(row):
    columns = row.find_all('div', class_='td')
    values = [column.find('div').text for column in columns]
    return parse_row(values)


def get_country_rows(soup):
    totals_header = soup.find('div', {'data-id': 'totals-header'})
    row_group_inner = totals_header.nextSibling.find('div').find('div')
    country_rows = row_group_inner.find_all(
        'div', {'class': 'tr', 'role': 'row'}
    )[2:]
    return country_rows


def get_column_names(soup):
    column_headers = (
        soup
        .find('div', class_='thead')
        .find('div', class_='tr')
        .find_all('div', class_='th')
    )
    column_names = [column_header.text for column_header in column_headers]
    return column_names


def get_column_totals(soup):
    totals_header = (
        soup
        .find('div', {'data-id': 'totals-header'})
        .find('div', class_='tr')
        .find_all('div', class_='th')
    )
    totals = [total.text for total in totals_header]
    return parse_row(totals)


def parse_row(row):
    parsed_row = row.copy()
    parsed_row[1:] = [_parse_string_as_number(value) for value in row[1:]]
    return parsed_row


def _parse_string_as_number(string):
    string_without_commas = string.replace(',', '')
    if not string_without_commas:
        return 0
    elif '.' in string_without_commas:
        return float(string_without_commas)
    else:
        return int(string_without_commas)


def get_page_source():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(WHO_COVID_DATA_URL)
    page_source = driver.page_source
    return driver, page_source


if __name__ == '__main__':
    covid_data = scrape()
    print(covid_data.head())
