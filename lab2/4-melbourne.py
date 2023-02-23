import pandas as pd
from matplotlib import pyplot as plt


def plot_relationship_between_price_and_size():
    plt.scatter(
        melbourne_data['Rooms'], melbourne_data['Price']
    )
    plt.xlabel('Number of rooms')
    plt.ylabel('Real estate price')
    plt.show()
    plt.scatter(
        melbourne_data['Bedroom2'], melbourne_data['Price']
    )
    plt.xlabel('Number of bedrooms')
    plt.ylabel('Real estate price')
    plt.show()
    plt.scatter(
        melbourne_data['Bedroom2'] + melbourne_data['Bathroom'],
        melbourne_data['Price']
    )
    plt.xlabel('Sum of number of bath- and bedrooms')
    plt.ylabel('Real estate price')
    plt.show()


def plot_property_counts_by_suburb():
    property_counts = melbourne_data.groupby(['Suburb']).count()[
        'Propertycount'].sort_values(ascending=False)
    property_counts.plot.bar()
    plt.xlabel('Suburbs')
    plt.ylabel('Property counts')
    plt.xticks([], [])
    plt.show()
    labels = ['' for x in property_counts]
    print(property_counts.head())
    num_suburb_names_to_show = 10
    labels[:num_suburb_names_to_show] = property_counts.index[
                                        :num_suburb_names_to_show]
    property_counts.plot.pie(labels=labels)
    plt.show()


if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')

    # Correlation between price and distance
    correlation = melbourne_data['Price'].corr(melbourne_data['Distance'])
    print(
        f"Correlation between the price and distance columns "
        f"is {correlation:.3f}."
    )

    # Scatter plot between size and price
    # plot_relationship_between_price_and_size()

    # Number of real estates per suburb
    plot_property_counts_by_suburb()