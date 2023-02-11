import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



# Connect to the MongoDB database
cluster = MongoClient("mongodb+srv://python_access:z2W7TOD2FAzDHXEd@cluster0.iiunhcg.mongodb.net/?retryWrites=true&w=majority")
db = cluster["D7054E"]
collection = db["covid2"]


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
y =  [covid_dict[key]["Name"] for key in keys]
x1 = [covid_dict[key]["Cases-cumulative total"] for key in keys]
x1 = [int(y) for y in x1]
x2 = [covid_dict[key]["Deaths-cumulative total"] for key in keys]
x2 = [int(y) for y in x2]



# Get percentage of deaths / cases
percentage = [format((deaths /cases *100),'.2f') for deaths, cases in zip(x2, x1)]

# Create the stacked bar plot
bar_height = 0.8
p1 = plt.barh(y, x1, bar_height, color='orange')
p2 = plt.barh(y, x2, bar_height, left=x1, color='r')

# Add the percentage next to the bars
for i, v in enumerate(x1):
    plt.annotate(str(percentage[i]) + " %" , xy=(v, i), xytext=(5, 0), textcoords='offset points', ha='left', va='center')


# Add legend and labels
plt.legend((p1[0], p2[0]), ('Cases-cumulative total', 'Deaths-cumulative total'))
plt.xlabel('Total cases  cumulative')
plt.ylabel('Countries')

# Define a function to format the x-axis labels
def format_func(value, tick_number):
    # Format the value with commas as the thousands separator
    return f'{value:,.0f}'

# Format the x-axis labels
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_func))



# Show the plot
plt.show()
