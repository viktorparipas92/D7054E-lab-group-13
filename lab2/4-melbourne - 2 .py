import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns



def plot_distance_price():
    # Task 1: Correlation between distance from CBD and prices of properties
    sns.regplot(x="Distance", y="Price", data=melbourne_data)
    plt.title("Distance vs Price")
    plt.show()


def plot_council_year():
    council_year = melbourne_data.groupby(['CouncilArea', 'YearBuilt']).size().reset_index( name='count' )
    council_year = council_year[council_year['YearBuilt'] >= 1800]

    top10_councils = council_year.groupby('CouncilArea')['count'].sum().nlargest(10).index
    council_year = council_year[council_year['CouncilArea'].isin(top10_councils)]

    sns.scatterplot(x='YearBuilt', y='count', hue='CouncilArea', data=council_year)
    plt.xlabel('Year Built')
    plt.ylabel('Number of Properties')
    plt.title('Number of Properties Built by Year and Council (Top 10)')
    plt.show()


def plot_seller_location():
    top_sellers = melbourne_data['SellerG'].value_counts().nlargest(5).index.tolist()
    seller_data = melbourne_data[melbourne_data['SellerG'].isin(top_sellers)]

    plt.figure(figsize=(10,8))
    for i, seller in enumerate(top_sellers):
        seller_subset = seller_data[seller_data['SellerG'] == seller]
        plt.scatter(seller_subset['Longtitude'], seller_subset['Lattitude'], alpha=0.5, label=seller, cmap='viridis')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Properties Sold by Top 5 Sellers')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')

    plot_distance_price()

    plot_council_year()

    plot_seller_location()