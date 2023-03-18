import pandas as pd


COLUMNS = [
    'Age',
    'DistanceFromHome',
    'MonthlyIncome',
    'NumCompaniesWorked',
    'PercentSalaryHike',
    'TotalWorkingYears',
    'TrainingTimesLastYear',
    'YearsAtCompany',
    'YearsSinceLastPromotion',
    'YearsWithCurrManager',
    'BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently',
    'BusinessTravel_Travel_Rarely',
    'Department_Human Resources', 'Department_Research & Development',
    'Department_Sales',
    'EducationField_Human Resources', 'EducationField_Life Sciences',
    'EducationField_Marketing', 'EducationField_Medical',
    'EducationField_Other', 'EducationField_Technical Degree',
    'Gender_Female', 'Gender_Male',
    'JobRole_Healthcare Representative', 'JobRole_Human Resources',
    'JobRole_Laboratory Technician', 'JobRole_Manager',
    'JobRole_Manufacturing Director',  'JobRole_Research Director',
    'JobRole_Research Scientist', 'JobRole_Sales Executive',
    'JobRole_Sales Representative',
    'MaritalStatus_Divorced', 'MaritalStatus_Married', 'MaritalStatus_Single',
    'OverTime_No', 'OverTime_Yes',
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