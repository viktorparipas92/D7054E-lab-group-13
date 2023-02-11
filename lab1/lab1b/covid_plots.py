import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Connect to Cloud  MongoDB database
cluster = MongoClient("mongodb+srv://python_access:z2W7TOD2FAzDHXEd@cluster0.iiunhcg.mongodb.net/?retryWrites=true&w=majority")
db = cluster["D7054E"]
collection = db["covid2"]


def create_bar_chart(collection):
    # Define the query as a dictionary
    query = {'Cases-cumulative total': {"$ne": ''}}

    # Retrieve the 15 countries with highest cases
    results = collection.find(query).sort('Cases-cumulative total', -1).limit(15)

    covid_dict = {}

    for result in results:
        # Get the "_id" field of the document
        doc_id = result["_id"]
        # Add the document to the dictionary with the "_id" field as the key
        covid_dict[doc_id] = result

    # Create lists for the x and y data
    keys = list(covid_dict.keys())
    y = [covid_dict[key]["Name"] for key in keys]
    x1 = [covid_dict[key]["Cases-cumulative total"] for key in keys]
    x1 = [int(y) for y in x1]
    x2 = [covid_dict[key]["Deaths-cumulative total"] for key in keys]
    x2 = [int(y) for y in x2]

    # Get percentage of deaths / cases
    percentage = [format((deaths / cases * 100), '.2f') for deaths, cases in zip(x2, x1)]

    # Create the stacked bar plot
    bar_height = 0.8
    p1 = plt.barh(y, x1, bar_height, color='orange')
    p2 = plt.barh(y, x2, bar_height, left=x1, color='r')
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)

    # Add the percentage next to the bars
    for i, v in enumerate(x1):
        plt.annotate(str(percentage[i]) + " %", xy=(v, i), xytext=(5, 0), textcoords='offset points', ha='left',
                     va='center', fontsize=16)

    # Add legend and labels
    plt.legend((p1[0], p2[0]), ('Cases-cumulative total', 'Deaths-cumulative total'), fontsize=14)
    plt.xlabel('Total cases  cumulative', fontsize=16)
    plt.ylabel('Countries', fontsize=16)

    # Define a function to format the x-axis labels
    def format_func(value, tick_number):
        # Format the value with commas as the thousands separator
        return f'{value:,.0f}'

    # Format the x-axis labels
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # Show the plot
    plt.show()

def create_scatterplot(collection):
    # Define the query as a dictionary
    query = {'Persons Boosted per 100 population': {"$ne": ''}}

    # Retrieve the documents that match the query
    results = collection.find(query)

    covid_dict = {}

    for result in results:
        # Get the "_id" field of the document
        doc_id = result["_id"]
        # Add the document to the dictionary with the "_id" field as the key
        covid_dict[doc_id] = result

    keys = list(covid_dict.keys())

    x = [covid_dict[key]["Persons fully vaccinated with last dose of primary series per 100 population"] for key in
         keys]
    y = [covid_dict[key]["Persons Boosted per 100 population"] for key in keys]
    name = [covid_dict[key]["Name"] for key in keys]
    z = [(y / x) * 1500 for y, x in zip(y, x)]
    colors = np.random.rand(16)

    cases = [covid_dict[key]["Cases-cumulative total"] for key in keys]
    deaths = [covid_dict[key]["Deaths-cumulative total"] for key in keys]
    percentage = [format((deaths / cases * 100), '.2f') for deaths, cases in zip(deaths, cases)]
    percentage = [float(key) for key in percentage]

    cmap = plt.cm.get_cmap('RdYlGn')
    cmap_reversed = cmap.reversed()
    # plt.scatter(x, y, s=z, c=colors, alpha=0.5,label='Boosted / Fully Vaccinated Percentage ')
    plt.scatter(x, y, s=500, c=percentage, cmap=cmap_reversed, alpha=0.5, label='Color - Infection Fatality Rate')

    plt.xlim(0, 100)  # set x-axis limits
    plt.ylim(0, 100)  # set x-axis limits
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)

    for i, txt in enumerate(name):
        plt.annotate(txt, (x[i], y[i]), fontsize=12)

    # for i, value in enumerate(percentage):
    #     plt.text(x[i], y[i], str(value), ha='right', va='top')

    # Add legend and labels
    plt.legend(loc='upper left')  # add the legend and specify its location

    plt.legend(fontsize=16)
    plt.xlabel('Persons fully vaccinated with last dose of primary series per 100 population', fontsize=16)
    plt.ylabel('Persons Boosted per 100 population', fontsize=16)

    # create a colorbar and set the font size of the text
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=16)

    plt.show()

def create_stacked_bar(collection):
    # Define the query as a dictionary
    query = {'Deaths-newly reported in last 7 days': {"$ne": ''}}

    # Retrieve the 15 countries with highest cases
    results = collection.find(query).limit(10)

    covid_dict = {}

    for result in results:
        # Get the "_id" field of the document
        doc_id = result["_id"]
        # Add the document to the dictionary with the "_id" field as the key
        covid_dict[doc_id] = result

    # Create lists for the x and y data
    keys = list(covid_dict.keys())

    deaths_cumulative = [covid_dict[key]["Deaths-cumulative total"] for key in keys]
    cases_cumulative = [covid_dict[key]["Cases-cumulative total"] for key in keys]
    mortality_rate_cumulative = [deaths / cases * 100 for deaths, cases in zip(deaths_cumulative, cases_cumulative)]

    deaths_week = [covid_dict[key]["Deaths-newly reported in last 7 days"] for key in keys]
    cases_week = [covid_dict[key]["Cases-newly reported in last 7 days"] for key in keys]
    mortality_rate_week = [deaths / cases * 100 for deaths, cases in zip(deaths_week, cases_week)]

    y = [covid_dict[key]["Name"] for key in keys]
    x1 = mortality_rate_cumulative
    x2 = mortality_rate_week

    # Define bar positions and bar width
    bar_width = 0.35
    bar_positions = range(len(mortality_rate_cumulative))

    # Create a grouped bar chart
    fig, ax = plt.subplots()
    rects1 = ax.bar(bar_positions, mortality_rate_week, bar_width, color='b', label='Infection Fatality Rate last week')
    rects2 = ax.bar([p + bar_width for p in bar_positions], mortality_rate_cumulative, bar_width, color='orange',
                    label='Infection Fatality Rate cumulative')

    # Add x-axis and y-axis labels and title
    ax.set_xlabel('Country', fontsize=16)
    ax.set_ylabel('Infection Fatality Rate (%)', fontsize=16)
    ax.set_title('Comparison of Infection Fatality Rates by country', fontsize=16)

    # Add x-axis tick labels
    ax.set_xticks([p + bar_width / 2 for p in bar_positions])
    ax.set_xticklabels(y)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)

    # Add a legend
    ax.legend(fontsize=16)

    plt.show()

if __name__ == '__main__':
    create_bar_chart(collection)
    create_scatterplot(collection)
    create_stacked_bar(collection)
    plt.show()