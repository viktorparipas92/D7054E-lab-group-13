import pandas as pd


FEATURES_TO_REMOVE = [
    'EmployeeNumber',
    'EmployeeCount',
    'Over18',
    'StandardHours',
]


def preprocess_attrition_data(dataset):
    # Convert Attrition column to binary 0/1
    dataset['Attrition'] = (dataset['Attrition'] == 'Yes').astype(int)

    categorical_variables = [
        'BusinessTravel',
        'Department',
        'EducationField',
        'Gender',
        'JobRole',
        'MaritalStatus',
        'OverTime',
    ]
    for column_name in categorical_variables:
        cat_list = pd.get_dummies(dataset[column_name], prefix=column_name)
        dataset = dataset.join(cat_list)

    # Create a list of independent variables ignoring some
    labels = dataset['Attrition']
    dataset.drop(FEATURES_TO_REMOVE, axis=1, inplace=True)
    dataset.drop(categorical_variables, axis=1, inplace=True)
    features = dataset.drop('Attrition', axis=1)
    return features, labels