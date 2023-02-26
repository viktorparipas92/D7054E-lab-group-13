from typing import List

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

from plot import create_plots
from scraping.scrape import get_page_source, parse_row, WebScraper

COOKIE_RECIPES_URL = 'https://openstax.org/books/introductory-statistics/pages/7-5-central-limit-theorem-cookie-recipes'
# Since 4 is A small sample size, i took 10 to make central limit theorem more apparent
NUMBER_OF_SAMPLES = 10


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


def calculate(table):
    mean = table['X'].mean()
    st_dev = table['X'].std()
    return mean, st_dev


def get_samples(table: pd.DataFrame, size: int) -> List[pd.Series]:
    samples = [table['X'].sample(n=size) for _ in range(NUMBER_OF_SAMPLES)]
    return samples


def get_mean_list(samples: List[pd.Series]):
    mean_list = [sample.mean() for sample in samples]
    sample_size = len(samples[0])

    print(
        f"Mean of sample means for sample size {sample_size}: "
        f"{float(statistics.mean(mean_list)):.2f}."
    )
    print(
        f"Standard deviation of sample means "
        f"for sample size {sample_size}: {statistics.stdev(mean_list):2f}."
    )
    return mean_list


def create_histogram(population, n=0):
    mean_list = mean_list_5 if n == 5 else mean_list_10 if n == 10 else []
    start = int(min(mean_list))
    stop = max(mean_list) + 2
    bin_edges = np.arange(start, stop, step=0.5)

    plt.hist(
        mean_list, bins=bin_edges, color='crimson', ec='white', rwidth=0.8
    )
    plt.plot(color='black', linewidth=2)
    plt.xticks(bin_edges, fontsize=16)

    largest_histogram_value = int(
        max(np.histogram(mean_list, bins=bin_edges)[0])
    )
    plt.yticks(np.arange(largest_histogram_value + 2), fontsize=16)
    plt.tight_layout()
    plt.title(f'Histogram for sample with size {str(n)}', fontsize=16)

    plt.xlabel('Days')
    plt.ylabel('Frequency')
    plt.show()


def _create_histogram_for_original_population(data):
    plt.hist(data, bins=range(1, 13), align='left', rwidth=0.8)
    plt.xticks(range(1, 13))
    plt.xlabel('Days')
    plt.ylabel('Frequency')
    plt.title('Histogram for original population')


def _create_histogram_for_sample_means(mean_list, n=5):
    start = int(min(mean_list))
    stop = max(mean_list) + 2
    bin_edges = np.arange(start, stop, step=0.5)

    plt.hist(
        mean_list, bins=bin_edges, color='crimson', ec='white', rwidth=0.8
    )
    plt.plot(color='black', linewidth=2)
    plt.xticks(bin_edges)

    largest_histogram_value = int(
        max(np.histogram(mean_list, bins=bin_edges)[0])
    )
    plt.yticks(np.arange(largest_histogram_value + 2))
    plt.title(f'Histogram for sample with size {str(n)}')

    plt.xlabel('Days')
    plt.ylabel('Frequency')


def _create_histogram_for_sample_size_5(mean_list):
    _create_histogram_for_sample_means(mean_list, n=5)


def _create_histogram_for_sample_size_10(mean_list):
    _create_histogram_for_sample_means(mean_list, n=10)


PLOT_TO_FILE_MAP_1 = {
    _create_histogram_for_original_population: 'cookie-recipe-histogram-original.png',
}

PLOT_TO_FILE_MAP_5 = {
    _create_histogram_for_sample_size_5: 'cookie-recipe-histogram-5.png',
}

PLOT_TO_FILE_MAP_10 = {
    _create_histogram_for_sample_size_10: 'cookie-recipe-histogram-10.png',
}


if __name__ == '__main__':
    driver, page_source = get_page_source(COOKIE_RECIPES_URL)
    soup = BeautifulSoup(page_source, features='html.parser')
    scraper = CookieRecipeScraper(soup)
    scraper.scrape()
    print(scraper.data.head())
    table = scraper.data

    # Task 1
    mean, standard_deviation = calculate(table)
    print(f'μx = {mean}')
    print(f'σx = {standard_deviation}')

    samples_5 = get_samples(table, 5)
    mean_list_5 = get_mean_list(samples_5)

    samples_10 = get_samples(table, 10)
    mean_list_10 = get_mean_list(samples_10)

    create_plots(table['X'], PLOT_TO_FILE_MAP_1, save_to_file=True)
    create_plots(mean_list_5, PLOT_TO_FILE_MAP_5, save_to_file=True)
    create_plots(mean_list_10, PLOT_TO_FILE_MAP_10, save_to_file=True)
