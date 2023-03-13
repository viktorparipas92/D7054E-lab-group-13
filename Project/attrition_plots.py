from Project.attrition_api import fetch_data

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from logistic_regresion_attrition import coef_df
import pandas as pd


def create_plot_coeff(coef_df):

    # Add labels and a title to the plot
    plt.xlabel('Coefficient Value')
    plt.ylabel('Feature')
    plt.title('Logistic Regression Coefficients')

    # Assign red color to coefficients greater than 0 and green color to coefficients greater than or equal to 0
    colors = ['green' if c > 0 else 'red' for c in coef_df['coefficient']]

    # Create a horizontal bar plot of the coefficients with the assigned colors
    plt.barh(coef_df['feature'], coef_df['coefficient'], color=colors)

    # Display the plot
    plt.show()



def create_plots(data):
    # Create a scatter plot of employee tenure vs attrition rate
    plt.scatter(attrition_df['YearsAtCompany'], attrition_df['Attrition'])
    plt.title('Employee Tenure vs Attrition Rate')
    plt.xlabel('YearsatCompany')
    plt.ylabel('Attrition')
    plt.show()

########################

    plt.hist(attrition_df['Age'], bins=30)
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.title('Age Distribution')
    plt.show()

########################

    sns.violinplot(x='Attrition', y='YearsAtCompany', hue='Gender', data=attrition_df, split=True)
    plt.title('Years at Company Distribution by Attrition and Gender')
    plt.show()

########################


    # Group the data by Attrition and calculate the mean of the three variables of interest
    attrition_means = attrition_df.groupby('Attrition')[
        ['YearsAtCompany', 'TotalWorkingYears', 'YearsSinceLastPromotion']].mean()

    # Create a stacked bar chart
    plt.bar(attrition_means.columns, attrition_means.loc["Yes"], label="Yes")
    plt.bar(attrition_means.columns, attrition_means.loc["No"], bottom=attrition_means.loc["Yes"], label="No")

    plt.title('Attrition')
    plt.xlabel('Variable')
    plt.ylabel('Average in Years')
    plt.legend()

    plt.show()


########################


    # Create a crosstab of Attrition and OverTime
    crosstab_df = pd.crosstab(attrition_df['Attrition'], attrition_df['OverTime'])

    # Plot the stacked bar chart
    crosstab_df.plot.bar(stacked=True)

    # Set the title and axis labels
    plt.title('Attrition by Overtime')
    plt.xlabel('Attrition')
    plt.ylabel('Employee Count')

    # Show the plot
    plt.show()



if __name__ == '__main__':
    attrition_df = fetch_data()
    create_plots(attrition_df)
    create_plot_coeff(coef_df)

