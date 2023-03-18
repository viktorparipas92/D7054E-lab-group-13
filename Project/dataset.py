from typing import Tuple

import numpy as np
import pandas as pd


FEATURES_TO_REMOVE = [
    'EmployeeNumber',
    'EmployeeCount',
    'Over18',
    'StandardHours',
]

NUMERICAL_CATEGORICAL_FEATURES = [
    'Education',
    'EnvironmentSatisfaction',
    'JobInvolvement',
    'JobLevel',
    'JobSatisfaction',
    'PerformanceRating',
    'RelationshipSatsifaction',
    'WorkLifeBalance',
    'StockOptionLevel',
]

TARGET = ['Attrition']


def split_into_categorical_and_numerical_data(dataset) -> Tuple[
    pd.DataFrame, pd.DataFrame
]:
    all_features = dataset.columns.tolist()
    numerical_features = dataset.select_dtypes(
        include=[np.int64, np.float64]
    ).columns.tolist()

    numerical_features = list(
        set(numerical_features) - set(NUMERICAL_CATEGORICAL_FEATURES)
    )
    categorical_features = list(
        set(all_features) - set(numerical_features) - set(TARGET)
    )

    return dataset[categorical_features], dataset[numerical_features]


def transform_numerical_features(numerical_features):
    column_names = numerical_features.columns.tolist()
    for column in column_names:
        if numerical_features[column].skew() > 0.80:
            numerical_features[column] = np.log1p(numerical_features[column])


def transform_categorical_features(categorical_features):
    column_names = categorical_features.columns.tolist()
    for col in column_names:
        column_dummies = pd.get_dummies(categorical_features[col], prefix=col)
        categorical_features = pd.concat(
            [categorical_features, column_dummies], axis=1
        )
    categorical_features.drop(column_names, axis=1, inplace=True)
    return categorical_features


def transform_target(dataset):
    attrition_target = dataset['Attrition'].map({'Yes': 1, 'No': 0})
    return attrition_target


def preprocess_attrition_data(dataset):
    dataset = dataset.copy()
    (
        categorical_data,
        numerical_data,
    ) = split_into_categorical_and_numerical_data(dataset)
    dataset.drop(FEATURES_TO_REMOVE, axis=1, inplace=True)

    transform_numerical_features(numerical_data)
    categorical_data = transform_categorical_features(categorical_data)
    final_dataset = pd.concat([numerical_data, categorical_data], axis=1)

    attrition_target = transform_target(dataset)

    return final_dataset, attrition_target
