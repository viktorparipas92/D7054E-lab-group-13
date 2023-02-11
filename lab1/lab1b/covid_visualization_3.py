import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



# Connect to the MongoDB database
cluster = MongoClient("mongodb+srv://python_access:z2W7TOD2FAzDHXEd@cluster0.iiunhcg.mongodb.net/?retryWrites=true&w=majority")
db = cluster["D7054E"]
collection = db["covid2"]


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
mortality_rate_cumulative = [ deaths/cases*100 for deaths, cases in zip(deaths_cumulative,cases_cumulative)]

deaths_week = [covid_dict[key]["Deaths-newly reported in last 7 days"] for key in keys]
cases_week = [covid_dict[key]["Cases-newly reported in last 7 days"] for key in keys]
mortality_rate_week = [ deaths/cases*100 for deaths, cases in zip(deaths_week,cases_week)]

y =  [covid_dict[key]["Name"] for key in keys]
x1 = mortality_rate_cumulative
x2 = mortality_rate_week



# Define bar positions and bar width
bar_width = 0.35
bar_positions = range(len(mortality_rate_cumulative))

# Create a grouped bar chart
fig, ax = plt.subplots()
rects1 = ax.bar(bar_positions, mortality_rate_week, bar_width, color='b', label='Infection Fatality Rate last week')
rects2 = ax.bar([p + bar_width for p in bar_positions], mortality_rate_cumulative, bar_width, color='orange', label='Infection Fatality Rate cumulative')

# Add x-axis and y-axis labels and title
ax.set_xlabel('Country')
ax.set_ylabel('Infection Fatality Rate (%)')
ax.set_title('Comparison of Infection Fatality Rates by country')

# Add x-axis tick labels
ax.set_xticks([p + bar_width / 2 for p in bar_positions])
ax.set_xticklabels(y)

# Add a legend
ax.legend()

plt.show()
