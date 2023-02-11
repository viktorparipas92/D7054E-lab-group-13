"""
Lab 1 will have two parts (A) and (B).
In Lab 1, you are required to implement in Python, the classes and objects.
A parent class will define the methods that will be inherited within the data
classes. You will do this together for the two datasets provided.

Part A
Python Basics: Object oriented concepts like inheritance, polymorphism:
You can use only 10 rows from each dataset.
Create a data structure for these two datasets, list different columns;
if it's a numeric value, show mean, variance and standard deviation.
You should be able to search for min and max values for each column.
For example, one data class represents the Happiness dataset and another
data class represents the COVID dataset.
Describe the data structures for example lists, sets, etc. that are used.

You are required to use the Draw IO online tool to draw the UML diagram for
your implementation and include in your report in the Appendix
"""
import csv
from contextlib import suppress
from dataclasses import dataclass
from itertools import islice

import numpy as np
import pandas as pd


class CSVLoader:
    def __init__(self, filename, max_number_of_rows=10, encoding=None):
        self.filename = filename
        self.max_number_of_rows = max_number_of_rows
        self.encoding = encoding
        self.data = []
        self.column_names = []
        self.type_map = {}

    def load_to_dict(self):
        with open(self.filename, 'r', encoding=self.encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self.column_names = csv_reader.fieldnames
            self.type_map = {cn: None for cn in self.column_names}
            self.data = [
                {k: self._convert_value(v, k) for k, v in row.items()}
                for row in islice(csv_reader, self.max_number_of_rows)
            ]

        return self.data

    def describe(self):
        for column_name in self.column_names:
            print(
                column_name,
                self.type_map.get(column_name),
                self.describe_column(column_name),
            )

    def to_dataclass(self, data_class):
        return [data_class(row) for row in self.data]

    def describe_column(self, column_name):
        column_values = self._get_column_by_name(column_name)
        if self.type_map.get(column_name) in (int, float):
            mean = np.mean(column_values)
            maximum_value = np.max(column_values)
            minimum_value = np.min(column_values)
            variance = np.var(column_values)
            standard_deviation = np.std(column_values)
            return {
                'mean': mean,
                'max': maximum_value,
                'min': minimum_value,
                'var': variance,
                'std': standard_deviation
            }
        else:
            return None

    def _get_column_by_name(self, column_name):
        return [row[column_name] for row in self.data]

    def _convert_value(self, value, column_name=None):
        column_type_from_map = self.type_map.get(column_name)
        if column_name is None or column_type_from_map is None:
            self.type_map[column_name] = self.infer_type(value)

        return self.type_map[column_name](value)

    @staticmethod
    def infer_type(value):
        types_to_try = [int, float]
        for type_ in types_to_try:
            with suppress(ValueError):
                value = type_(value)
                return type_

        return str


@dataclass
class Data:
    mapping = {}

    def from_csv_row(self, csv_row: dict):
        mapping = {v: k for k, v in self.mapping.items()}
        for column_name, value in csv_row.items():
            dataclass_field = mapping.get(column_name)
            setattr(self, dataclass_field, value)


@dataclass
class CovidData(Data):
    name: str
    region: str
    total_cases: int
    total_cases_per_million: float
    cases_last_week: int
    cases_last_day: int
    total_deaths: int
    total_deaths_per_million: float
    deaths_last_week: int
    deaths_last_day: int
    transmission: str

    mapping = {
        'name': 'Name',
        'region': 'WHO Region',
        'total_cases': 'Cases - cumulative total',
        'total_cases_per_million': 'Cases - cumulative total per 1 million population',
        'cases_last_week': 'Cases - newly reported in last 7 days',
        'cases_last_day': 'Cases - newly reported in last 24 hours',
        'total_deaths': 'Deaths - cumulative total',
        'total_deaths_per_million': 'Deaths - cumulative total per 1 million population',
        'deaths_last_week': 'Deaths - newly reported in last 7 days',
        'deaths_last_day': 'Deaths - newly reported in last 24 hours',
        'transmission': 'Transmission Classification',
    }

    def __init__(self, csv_row):
        super().from_csv_row(csv_row)


class HappinessData(Data):
    overall_rank: int
    country_or_region: str
    score: float
    gdp_per_capita: float
    social_support: float
    life_expectancy: float
    freedom_of_choice: float
    generosity: float
    corruption_perception: float

    mapping = {
        'overall_rank': 'Overall rank',
        'country_or_region': 'Country or region',
        'score': 'Score',
        'gdp_per_capita': 'GDP per capita',
        'social_support': 'Social support',
        'life_expectancy': 'Healthy life expectancy',
        'freedom_of_choice': 'Freedom to make life choices',
        'generosity': 'Generosity',
        'corruption_perception': 'Perceptions of corruption',
    }

    def __init__(self, csv_row):
        super().from_csv_row(csv_row)


if __name__ == '__main__':
    covid_filename = '../datasets/WHO COVID-19 data.csv'
    happiness_filename = '../datasets/World_Happiness_2019.csv'

    # For reference
    covid_data = pd.read_csv(covid_filename)
    happiness_data = pd.read_csv(happiness_filename)
    covid_data.describe()

    covid_loader = CSVLoader(covid_filename, encoding='utf-8-sig')
    covid_loader.load_to_dict()
    covid_loader.describe()
    covid_datapoints = covid_loader.to_dataclass(CovidData)

    happiness_loader = CSVLoader(happiness_filename)
    happiness_loader.load_to_dict()
    happiness_loader.describe()
    happiness_datapoints = happiness_loader.to_dataclass(HappinessData)




