from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import norm

from scraping.scrape import get_page_source, parse_row, WebScraper
from plot import create_plots

LAP_TIMES_URL = 'https://openstax.org/books/introductory-statistics/pages/c-data-sets'


class LapTimeScraper(WebScraper):
    def get_table(self):
        return (
            self.soup
            .find('div', {'data-type': 'page'})
            .find('h2', string='Lap Times')
            .parent
            .find('div')
            .find('table')
        )

    def _set_table(self, table):
        self.table = table

    def get_column_names(self):
        column_headers = self.table.find('thead').find('tr').find_all('th')
        column_names = [column_header.text for column_header in
                        column_headers[1:]]
        return column_names

    def get_rows(self):
        rows = self.table.find('tbody').find_all('tr')
        return rows

    def scrape(self):
        table = self.get_table()
        self._set_table(table)

        column_names = self.get_column_names()
        lap_times = pd.DataFrame(columns=column_names)

        rows = self.get_rows()
        for row in rows:
            values = [column.text for column in row.find_all('td')]
            parsed_values = parse_row(values)
            lap_times.loc[len(lap_times.index)] = parsed_values[1:]

        indices = [row.find('td').text for row in rows]
        lap_times.index = indices

        self.data = lap_times


def sample(data, laps_per_race=6):
    all_sampled_laps = np.array([])
    for _, row in data.iterrows():
        sampled_laps = np.random.choice(row, laps_per_race)
        all_sampled_laps = np.concatenate((all_sampled_laps, sampled_laps))

    return all_sampled_laps


def _plot_histogram(data):
    plt.hist(data, bins=6)
    plt.xlabel('Time [s]')
    plt.ylabel('Occurrence')
    plt.title('Histogram of lap times')


def _plot_distribution(data):
    sns.distplot(data)
    plt.xlabel('Time [s]')
    plt.ylabel('Density')
    plt.title('Density plot of lap times')
    print("The graph has a bell shape.")


def collect():
    driver, page_source = get_page_source(LAP_TIMES_URL)
    soup = BeautifulSoup(page_source, features='html.parser')
    scraper = LapTimeScraper(soup)
    scraper.scrape()
    lap_times = scraper.data

    sample_lap_times = sample(lap_times)
    # samples_from_laps_2_to_7 = sample_lap_times[6:42]
    mean = sample_lap_times.mean()
    std = sample_lap_times.std()
    print(f"The mean lap time is {mean:.2f}")
    print(f"The standard deviation of lap times is {std:.2f}")
    return lap_times, sample_lap_times, mean, std


def analyze(mean, std):
    print(
        f"The lap times seem to be normally distributed "
        f"around mean {mean:.2f} "
        f"with a standard deviation of {std:.2f}\n"
        f"The histogram and the associated density plot's graph "
        f"resembles the PDF of the Gaussian normal distribution."
    )


def describe(data):
    quartile_1 = np.quantile(data, 0.25)
    quartile_3 = np.quantile(data, 0.75)
    iqr = quartile_3 - quartile_1
    print(
        f"The inter-quartile range is {iqr} "
        f"going from {quartile_1} to {quartile_3}."
    )

    percentile_15 = np.quantile(data, 0.15)
    percentile_85 = np.quantile(data, 0.85)
    print(
        f"The 15th and 85th percentile are "
        f"{percentile_15} and {percentile_85}, respectively."
    )

    median = np.median(data)
    print(
        f"The median of the lap times is {median}."
    )

    p_over_130 = len(data[data > 130]) / len(data)
    print(
        f"The empirical probability that the lap time is over 130 seconds is "
        f"{p_over_130:.4f}"
    )


def theoretical(mean, std):
    distribution = norm(mean, std)
    quartile_1 = distribution.ppf(0.25)  # inverse of CDF
    quartile_3 = distribution.ppf(0.75)
    iqr = quartile_3 - quartile_1
    print(
        f"The theoretical inter-quartile range is {iqr:.2f} "
        f"going from {quartile_1:.2f} to {quartile_3:.2f}."
    )

    percentile_15 = distribution.ppf(0.15)
    percentile_85 = distribution.ppf(0.85)
    print(
        f"The theoretical 15th and 85th percentile are "
        f"{percentile_15:.2f} and {percentile_85:.2f}, respectively."
    )

    median = distribution.ppf(0.5)
    print(
        f"The theoretical median of the lap times is {median:.2f}."
    )

    p_over_130 = distribution.sf(130)  # complementary CDF
    print(
        f"The theoretical probability that the lap time is over 130 seconds is "
        f"{p_over_130:.4f}"
    )

    print(
        "The meaning of the 85th percentile of this dataset "
        "is that 85% of the lap times in the dataset are lower than this value "
        "while the remaining 15% are higher.\n"
        "In terms of the theoretical distribution, the cumulative distribution "
        "function's value is 0.85 at the 85th percentile."
    )


PLOT_TO_FILE_MAP = {
    _plot_histogram: 'normal-histogram.png',
    _plot_distribution: 'normal-distplot.png',
}


if __name__ == '__main__':
    lap_times, sample_lap_times, mean, std = collect()
    analyze(mean, std)
    describe(sample_lap_times)
    theoretical(mean, std)
    create_plots(sample_lap_times, PLOT_TO_FILE_MAP, save_to_file=True)



