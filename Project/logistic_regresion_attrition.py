from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from attrition_api import fetch_data
import matplotlib.pyplot as plt
import pandas as pd


def train_logistic_regression(df, columns):
    df['Attrition'] = (df['Attrition'] == 'Yes').astype(int)
    cat_vars = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
    for var in cat_vars:
        cat_list = pd.get_dummies(df[var], prefix=var)
        df = df.join(cat_list)

    x = df[columns]
    y = df['Attrition']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=23)
    lr = LogisticRegression(solver='lbfgs', max_iter=2500)
    lr.fit(x_train, y_train)

    y_pred = lr.predict(x_test)

    accur = lr.score(x_test, y_test)

    coef = lr.coef_[0]

    coef_dataframe = pd.DataFrame({'feature': columns, 'coefficient': coef})

    coef_dataframe = coef_dataframe.sort_values(by='coefficient', ascending=False)

    return lr, y_pred, accur, coef_dataframe


def create_plot_coeff(coef_dataframe):

    plt.xlabel('Coefficient Value')
    plt.ylabel('Feature')
    plt.title('Logistic Regression Coefficients')
    colors = ['green' if c > 0 else 'red' for c in coef_df['coefficient']]
    plt.barh(coef_dataframe['feature'], coef_dataframe['coefficient'], color=colors)
    plt.show()


if __name__ == '__main__':
    attrition_df = fetch_data()
    cols = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears',
            'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
            'BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
            'Department_Human Resources', 'Department_Research & Development', 'Department_Sales',
            'EducationField_Human Resources', 'EducationField_Life Sciences', 'EducationField_Marketing',
            'EducationField_Medical', 'EducationField_Other', 'EducationField_Technical Degree', 'Gender_Female',
            'Gender_Male', 'JobRole_Healthcare Representative', 'JobRole_Human Resources',
            'JobRole_Laboratory Technician', 'JobRole_Manager', 'JobRole_Manufacturing Director',
            'JobRole_Research Director', 'JobRole_Research Scientist', 'JobRole_Sales Executive',
            'JobRole_Sales Representative', 'MaritalStatus_Divorced', 'MaritalStatus_Married', 'MaritalStatus_Single',
            'OverTime_No', 'OverTime_Yes', "StockOptionLevel"]

    log_r, Y_pred, accuracy, coef_df = train_logistic_regression(attrition_df, cols)

    print('Accuracy:', accuracy)
    print(coef_df)
    create_plot_coeff(coef_df)
