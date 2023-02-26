import pandas as pd
import seaborn as sns
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
    plt.ylabel('Real estate price [AUD]')


def _plot_property_counts_by_suburb(melbourne_data):
    property_counts = melbourne_data.groupby(['Suburb']).count()[
        'Propertycount'].sort_values(ascending=False)
    # property_counts.plot.bar()
    plt.xlabel('Suburbs')
    plt.ylabel('Property counts')
    plt.xticks([], [])

    labels = ['' for x in property_counts]
    num_suburb_names_to_show = 10
    labels[:num_suburb_names_to_show] = (
        property_counts.index[:num_suburb_names_to_show]
    )
    property_counts.plot.pie(labels=labels)


def _plot_relationship_between_distance_and_price(melbourne_data):
    correlation = melbourne_data['Price'].corr(melbourne_data['Distance'])
    print(
        f"Correlation between the price and distance columns "
        f"is {correlation:.3f}."
    )

    sns.regplot(x='Distance', y='Price', data=melbourne_data)
    plt.xlabel('Distance [km?]')
    plt.ylabel('Price [AUD]')
    plt.title('Distance vs Price')


def _plot_properties_by_council_and_year_built(melbourne_data):
    counts_by_council_and_year = melbourne_data.groupby(
        ['CouncilArea', 'YearBuilt']
    ).size().reset_index(name='count')
    counts_by_council_and_year_after_1800 = (
        counts_by_council_and_year[
            counts_by_council_and_year['YearBuilt'] >= 1800
        ]
    )

    top10_councils = counts_by_council_and_year_after_1800.groupby(
        'CouncilArea'
    )['count'].sum().nlargest(10).index
    counts_by_top_10_council_and_year_after_1800 = (
        counts_by_council_and_year_after_1800[
            counts_by_council_and_year_after_1800['CouncilArea']
            .isin(top10_councils)
        ]
    )

    sns.scatterplot(
        x='YearBuilt',
        y='count',
        hue='CouncilArea',
        data=counts_by_top_10_council_and_year_after_1800,
    )
    plt.xlabel('Year Built')
    plt.ylabel('Number of Properties')
    plt.title('Number of Properties Built by Year and Council (Top 10)')


def _plot_seller_location(melbourne_data):
    top_sellers = (
        melbourne_data['SellerG'].value_counts()
        .nlargest(5)
        .index
        .tolist()
    )
    seller_data = melbourne_data[melbourne_data['SellerG'].isin(top_sellers)]

    plt.figure(figsize=(10, 8))
    for top_seller in top_sellers:
        seller_subset = seller_data[seller_data['SellerG'] == top_seller]
        plt.scatter(
            seller_subset['Longtitude'],
            seller_subset['Latitude'],
            alpha=0.5, label=top_seller, cmap='viridis',
        )

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Properties Sold by Top 5 Sellers')
    plt.legend()


PLOT_TO_FILE_MAP = {
    _plot_relationship_between_distance_and_price: 'melbourne-corr-distance.png',
    _plot_property_counts_by_suburb: 'melbourne-properties-per-suburb.png',
    _plot_relationship_between_price_and_size: 'melbourne-scatter-size.png',
    _plot_properties_by_council_and_year_built: 'melbourne-scatter-yearbuilt.png',
    _plot_seller_location: 'melbourne-seller-location.png',
}


if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')

    create_plots(melbourne_data, PLOT_TO_FILE_MAP, save_to_file=True)
