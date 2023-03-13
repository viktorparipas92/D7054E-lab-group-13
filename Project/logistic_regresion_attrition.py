import pandas as pd
import statsmodels.api as sm
from attrition_api import fetch_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

attrition_df = fetch_data()
# Convert Attrition column to binary 0/1
attrition_df['Attrition'] = (attrition_df['Attrition'] == 'Yes').astype(int)

# Create variables for categorical variables to turn to numerical
cat_vars = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
for var in cat_vars:
    cat_list = f'var_{var}'
    cat_list = pd.get_dummies(attrition_df[var], prefix=var)
    attrition_df = attrition_df.join(cat_list)

# Create a list of independent variables ignoring some
cols = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike',
            'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion',
            'YearsWithCurrManager', 'BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently',
            'BusinessTravel_Travel_Rarely', 'Department_Human Resources', 'Department_Research & Development',
            'Department_Sales', 'EducationField_Human Resources', 'EducationField_Life Sciences',
            'EducationField_Marketing', 'EducationField_Medical', 'EducationField_Other',
            'EducationField_Technical Degree', 'Gender_Female', 'Gender_Male', 'JobRole_Healthcare Representative',
            'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager',
            'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
            'JobRole_Sales Executive', 'JobRole_Sales Representative', 'MaritalStatus_Divorced',
            'MaritalStatus_Married', 'MaritalStatus_Single', 'OverTime_No', 'OverTime_Yes']

X = attrition_df[cols]
Y = attrition_df['Attrition']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# Train a logistic regression model
lr = LogisticRegression(solver='lbfgs',max_iter=2500)
lr.fit(X_train, Y_train)

# Predict on the test set
Y_pred = lr.predict(X_test)

# Evaluate the model on the test set
accuracy = lr.score(X_test, Y_test)
print('Accuracy:', accuracy)

# Get the coefficients from the logistic regression model
coef = lr.coef_[0]

# Create a pandas DataFrame with the coefficients and feature names
coef_df = pd.DataFrame({'feature': cols, 'coefficient': coef})
# Sort the DataFrame by the value of the coefficient in descending order
coef_df = coef_df.sort_values(by='coefficient', ascending=False)
# Print the DataFrame
print(coef_df)