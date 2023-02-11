from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np



# Connect to the MongoDB database
cluster = MongoClient("mongodb+srv://python_access:z2W7TOD2FAzDHXEd@cluster0.iiunhcg.mongodb.net/?retryWrites=true&w=majority")
db = cluster["D7054E"]
collection = db["covid2"]


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

x = [covid_dict[key]["Persons fully vaccinated with last dose of primary series per 100 population"] for key in keys]
y = [covid_dict[key]["Persons Boosted per 100 population"] for key in keys]
name = [covid_dict[key]["Name"] for key in keys]
z = [(y /x)*1500 for y, x in zip(y, x)]
colors = np.random.rand(16)

cases = [covid_dict[key]["Cases-cumulative total"] for key in keys]
deaths =  [covid_dict[key]["Deaths-cumulative total"] for key in keys]
percentage = [format((deaths /cases *100),'.2f') for deaths, cases in zip(deaths, cases)]
percentage = [float(key)  for key in percentage]

cmap = plt.cm.get_cmap('RdYlGn')
cmap_reversed = cmap.reversed()
# plt.scatter(x, y, s=z, c=colors, alpha=0.5,label='Boosted / Fully Vaccinated Percentage ')
plt.scatter(x, y,s = 500, c=percentage,cmap =  cmap_reversed, alpha=0.5,label='Color - Infection Fatality Rate')

# plt.scatter(x, y)
plt.xlim(0, 100)  # set x-axis limits
plt.ylim(0, 100)  # set x-axis limits


for i, txt in enumerate(name):
    plt.annotate(txt, (x[i], y[i])  )

# for i, value in enumerate(percentage):
#     plt.text(x[i], y[i], str(value), ha='right', va='top')

# Add legend and labels
plt.legend(loc='upper left')  # add the legend and specify its location

plt.legend()
plt.xlabel('Persons fully vaccinated with last dose of primary series per 100 population')
plt.ylabel('Persons Boosted per 100 population')


plt.show()
