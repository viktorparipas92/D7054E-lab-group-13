from abc import ABC

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse_row(row, index_as_number=False):
    parsed_row = row.copy()
    if index_as_number:
        parsed_row = [_parse_string_as_number(value) for value in row]
    else:
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


def get_page_source(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    return driver, page_source


class WebScraper(ABC):
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.table = None
        self.data = None

    def scrape(self):
        raise NotImplementedError

    def get_table(self):
        raise NotImplementedError

    def get_column_names(self):
        raise NotImplementedError

    def get_rows(self):
        raise NotImplementedError
