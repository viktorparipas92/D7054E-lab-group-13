# Part 1A
The file `lab1a.py` can be run as a script which loads 
the CSV files first into a list of dictionaries (the data 
attribute of the csv loader), and then to an instance of
the respective dataclass. The script also prints the statistical
attributes of the datasets.

# Part 1B
## Web scraping
The file `covid_webscraping.py` can be run as a script which
scrapes the page and stores the dataset in a dataframe, and prints
the first 5 rows.
The script `happiness_webscraping.py` on the other hand stores
the scraped dataset in a list of dictionaries, and prints the list.

## API
The files `covid_api.py` and `happiness_api.py` can be run as scripts
which call the Kaggle API to retrieve the respective datasets and
store them in a dataframe. Credentials hard-coded in the code.
(Not good practice, we know.)

## CSV loading and MongoDB storage
The file `database.py` can be run as a script which loads the
dataset from the .csv file in the file system and stores it
in a local MongoDB database. Further instructions on how to install
and run MongoDB locally in

## Visualization
The following files generate all the plots:
- `happiness_plots.py`
- `covid_visualization_1.py`
- `covid_visualization_2.py`
- `covid_visualizatioh_3.py`


For the happiness plots, the dataset is fetched through the Kaggle
API, while for the covid plots, the dataset is fetched from
MongoDB in the cloud. (Not read from the local database)

