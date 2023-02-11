from typing import Dict, List

import pymongo

from lab1a import CSVLoader, COVID_FILENAME, HAPPINESS_FILENAME


DATABASE_NAME = 'lab-1'


def save_to_database(data: List[Dict], collection_name: str):
    mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')

    lab_1_database = mongo_client[DATABASE_NAME]
    collection = lab_1_database[collection_name]
    if collection_name in lab_1_database.list_collection_names():
        last_row = collection.find_one(data[-1])
        if last_row is not None and len(list(collection.find())) == len(data):
            print(f"Data already in collection {collection_name}")
            return collection

    collection.insert_many(data)
    return collection


if __name__ == '__main__':
    covid_loader = CSVLoader(COVID_FILENAME, encoding='utf-8-sig')
    covid_loader.load_to_dict()
    covid_data = covid_loader.data
    covid_collection = save_to_database(covid_data, 'covid')
    print(covid_collection.find(covid_data[0]))

    happiness_loader = CSVLoader(HAPPINESS_FILENAME)
    happiness_loader.load_to_dict()
    happiness_data = happiness_loader.data
    happiness_collection = save_to_database(happiness_data, 'happiness')
    print(covid_collection.find(happiness_data[0]))
