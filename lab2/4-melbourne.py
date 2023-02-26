import pandas as pd
from matplotlib import pyplot as plt

from plot import create_plots


def _plot_relationship_between_price_and_size(melbourne_data, variant=2):
    if variant == 0:
        x = melbourne_data['Rooms']
        plt.xlabel('Number of rooms')
    elif variant == 1:
        x = melbourne_data['Bedroom2']
        plt.xlabel('Number of bedrooms')
    elif variant == 2:
        x = melbourne_data['Bedroom2'] + melbourne_data['Bathroom']
        plt.xlabel('Sum of number of bath- and bedrooms')
    else:
        return

    plt.scatter(x, melbourne_data['Price'])
    plt.ylabel('Real estate price')


def _plot_property_counts_by_suburb(melbourne_data):
    property_counts = melbourne_data.groupby(['Suburb']).count()[
        'Propertycount'].sort_values(ascending=False)
    # property_counts.plot.bar()
    plt.xlabel('Suburbs')
    plt.ylabel('Property counts')
    plt.xticks([], [])

    labels = ['' for x in property_counts]
    num_suburb_names_to_show = 10
    labels[:num_suburb_names_to_show] = property_counts.index[
                                        :num_suburb_names_to_show]
    property_counts.plot.pie(labels=labels)


def _plot_correlation_between_distance_and_price(melbourne_data):
    correlation = melbourne_data['Price'].corr(melbourne_data['Distance'])
    print(
        f"Correlation between the price and distance columns "
        f"is {correlation:.3f}."
    )


PLOT_TO_FILE_MAP = {
    _plot_correlation_between_distance_and_price: 'melbourne-corr-distance.png',
    _plot_property_counts_by_suburb: 'melbourne-properties-per-suburb.png',
    _plot_relationship_between_price_and_size: 'melbourne-scatter-size.png'
}


if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')

    create_plots(melbourne_data, PLOT_TO_FILE_MAP, save_to_file=True)
