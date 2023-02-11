from happiness_api import fetch_data

import matplotlib.pyplot as plt
import numpy as np


def create_plots(data):
    plt.matshow(data.drop('Overall rank', axis=1).corr())
    plt.colorbar(location='right', shrink=0.8)
    plt.xlabel('Dataset indices')
    plt.ylabel('Dataset indices')
    plt.title('Correlation coefficient between columns')
    plt.show()

    _create_line_plot(data)
    _create_bar_chart(data)
    _create_heatmap(data)
    _create_scatter_plot(data)


def _create_line_plot(data):
    plt.hist(data['Score'], bins=14)
    plt.hist(data['Generosity'], bins=14)
    plt.show()


def _create_bar_chart(data):
    n = num_countries_to_show = 10
    plt.subplots()
    happiest_countries = data['Country or region'][:n]
    gdp = data['GDP per capita'][:n]
    ss = data['Social support'][:n]
    hle = data['Healthy life expectancy'][:n]
    freedom = data['Freedom to make life choices'][:n]
    generosity = data['Generosity'][:n]
    poc = data['Perceptions of corruption'][:n]

    plt.bar(happiest_countries, gdp, label='GDP/capita')
    plt.bar(
        happiest_countries, ss, bottom=gdp, label='Social support',
    )
    plt.bar(
        happiest_countries, hle,
        bottom=ss + gdp,
        label='Healthy life expectancy',
    )
    plt.bar(
        happiest_countries, freedom,
        bottom=ss + gdp + hle,
        label='Freedom to make life choices',
    )
    plt.bar(
        happiest_countries, generosity,
        bottom=ss + gdp + hle + freedom,
        label='Generosity',
    )
    plt.bar(
        happiest_countries, poc,
        bottom=ss + gdp + hle + freedom + generosity,
        label='Perceptions of corruption',
    )
    plt.bar(
        happiest_countries, data['Score'][:n],
        label='Total score',
        edgecolor='black',
        color='white',
        alpha=0.2,
    )
    plt.xticks(rotation=60)
    plt.legend(loc='right')
    plt.show()


def _create_heatmap(data):
    plt.hist2d(
        data['Generosity'],
        data['GDP per capita'],
        cmap=plt.cm.copper,
    )
    plt.xlabel('Happiness as explained by generosity')
    plt.ylabel('Happiness as explained by GDP per capita')
    plt.title('2D histogram of countries')
    plt.colorbar()
    plt.show()


def _create_scatter_plot(data):
    min_happiness = 0
    max_happiness = 8
    happiness_explained = (
        data['GDP per capita']
        + data['Social support']
        + data['Healthy life expectancy']
        + data['Freedom to make life choices']
        + data['Generosity']
        + data['Perceptions of corruption']
    )
    plt.title('Explainable and ineffable happiness')
    plt.scatter(happiness_explained, data['Score'], label='Countries')
    plt.xlabel('Happiness explained (sum of factors)')
    plt.xticks(np.arange(min_happiness, max_happiness, 1))
    plt.ylabel('Overall happiness score')
    plt.yticks(np.arange(min_happiness, max_happiness, 1))
    plt.plot(
        [min_happiness, max_happiness],
        [min_happiness, max_happiness],
        label='$y = x$',
        color='green',
    )
    # Trendline
    line_coefficients = np.polyfit(happiness_explained, data['Score'], 1)
    polynomial_1d = np.poly1d(line_coefficients)

    # add trendline to plot
    plt.plot(
        happiness_explained,
        polynomial_1d(happiness_explained),
        label=f'Linear fit: $y = {line_coefficients[0]:.2f}x + '
              f'{line_coefficients[1]:.2f}$',
        color='red',
    )
    plt.legend(loc='lower right')


if __name__ == '__main__':
    happiness_data = fetch_data()
    create_plots(happiness_data)
    plt.show()