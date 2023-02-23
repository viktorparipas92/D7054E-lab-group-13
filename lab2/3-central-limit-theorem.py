import pandas as pd
from bs4 import BeautifulSoup

from scraping.scrape import get_page_source, parse_row, WebScraper

COOKIE_RECIPES_URL = 'https://openstax.org/books/introductory-statistics/pages/7-5-central-limit-theorem-cookie-recipes'


class CookieRecipeScraper(WebScraper):
    def scrape(self):
        table = self.get_table()
        self._set_table(table)
        column_names = self.get_column_names()
        cookie_recipes = pd.DataFrame(columns=column_names)
        self.data = cookie_recipes

        rows = self.get_rows()
        for row in rows:
            values = [column.text for column in row.find_all('td')]
            parsed_split_rows = self._parse_recipe_row(values)
            for split_row in parsed_split_rows:
                self.data.loc[len(self.data.index)] = split_row

        self.data.set_index(column_names[0], inplace=True)
        self.data.sort_index(inplace=True)

    @staticmethod
    def _parse_recipe_row(row):
        split_rows = [
            row[0:2], row[3:5], row[6:8], row[9:]
        ]
        return [parse_row(row, index_as_number=True) for row in split_rows]

    def get_table(self):
        return (
            self.soup.find('table', {'data-id': 'tableones23'})
        )

    def _set_table(self, table):
        self.table = table

    def get_column_names(self):
        first_column_header = self.table.find('thead').find('tr').find('th')
        second_column_header = self.table.select_one('th em')
        column_headers = (first_column_header, second_column_header)
        column_names = [column_header.text for column_header in column_headers]
        return column_names

    def get_rows(self):
        rows = self.table.find('tbody').find_all('tr')
        return rows


if __name__ == '__main__':
    driver, page_source = get_page_source(COOKIE_RECIPES_URL)
    soup = BeautifulSoup(page_source, features='html.parser')
    scraper = CookieRecipeScraper(soup)
    scraper.scrape()
    print(scraper.data.head())
