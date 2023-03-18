from matplotlib import pyplot as plt

from attrition_api import fetch_data

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


COLUMNS = [
    'Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked',
    'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
    'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
    'BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently',
    'BusinessTravel_Travel_Rarely', 'Department_Human Resources',
    'Department_Research & Development', 'Department_Sales',
    'EducationField_Human Resources', 'EducationField_Life Sciences',
    'EducationField_Marketing', 'EducationField_Medical',
    'EducationField_Other', 'EducationField_Technical Degree',
    'Gender_Female', 'Gender_Male', 'JobRole_Healthcare Representative',
    'JobRole_Human Resources', 'JobRole_Laboratory Technician',
    'JobRole_Manager', 'JobRole_Manufacturing Director',
    'JobRole_Research Director', 'JobRole_Research Scientist',
    'JobRole_Sales Executive', 'JobRole_Sales Representative',
    'MaritalStatus_Divorced', 'MaritalStatus_Married',
    'MaritalStatus_Single', 'OverTime_No', 'OverTime_Yes',
]


def preprocess_attrition_data(dataset, columns=None):
    columns = columns or COLUMNS
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
    features = dataset[columns]
    labels = dataset['Attrition']
    return features, labels


def get_coefficient_dataframe(model):
    coefficients = model.coef_[0]
    coefficient_df = pd.DataFrame(
        {'feature': COLUMNS, 'coefficient': coefficients}
    )
    coefficient_df = coefficient_df.sort_values(
        by='coefficient', ascending=False
    )
    return coefficient_df


def train_logistic_regression(df, columns=None):
    columns = columns or COLUMNS
    x, y = preprocess_attrition_data(df, columns)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.1, random_state=23
    )
    logistic_regression = LogisticRegression(solver='lbfgs', max_iter=2500)
    logistic_regression.fit(x_train, y_train)
    y_predicted = logistic_regression.predict(x_test)

    accuracy = logistic_regression.score(x_test, y_test)

    coefficient_dataframe = get_coefficient_dataframe(logistic_regression)

    return logistic_regression, y_predicted, accuracy, coefficient_dataframe


def create_plot_coefficients(coef_df):
    plt.xlabel('Coefficient Value')
    plt.ylabel('Feature')
    plt.title('Logistic Regression Coefficients')

    colors = ['green' if c > 0 else 'red' for c in coef_df['coefficient']]
    plt.barh(coef_df['feature'], coef_df['coefficient'], color=colors)
    plt.show()


if __name__ == '__main__':
    attrition_dataset = fetch_data()

    (
        logistic_regression,
        y_predicted,
        accuracy,
        coefficient_dataframe,
    ) = train_logistic_regression(attrition_dataset)

    print('Accuracy:', accuracy)
    print(coefficient_dataframe)

    create_plot_coefficients(coefficient_dataframe)
