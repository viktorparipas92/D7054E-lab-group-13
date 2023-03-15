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
    plt.xlabel('YearsatCompany',fontsize=16)
    plt.ylabel('Attrition',fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.show()

########################

    # Separate the age data by attrition status
    attrition_yes = attrition_df[attrition_df['Attrition'] == 'Yes']['Age']
    attrition_no = attrition_df[attrition_df['Attrition'] == 'No']['Age']

    # Create a histogram with two sets of bars
    plt.hist([attrition_yes, attrition_no], bins=30, color=['red', 'blue'], label=['Attrition: Yes', 'Attrition: No'])

    # Add axis labels and title
    plt.xlabel('Age', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Age Distribution by Attrition Status')

    # Add a legend and show the plot
    plt.legend()
    plt.show()

########################

    sns.violinplot(x='Attrition', y='YearsAtCompany',fontsize=16, hue='Gender', data=attrition_df, split=True)
    plt.title('Years at Company Distribution by Attrition and Gender')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.show()

########################


    # Group the data by Attrition and calculate the mean of the three variables of interest
    attrition_means = attrition_df.groupby('Attrition')[
        ['YearsAtCompany', 'TotalWorkingYears', 'YearsSinceLastPromotion']].mean()

    # Create a stacked bar chart
    plt.bar(attrition_means.columns, attrition_means.loc["No"], label="No")
    plt.bar(attrition_means.columns, attrition_means.loc["Yes"], bottom=attrition_means.loc["No"], label="Yes")

    plt.title('Attrition')
    plt.xlabel('Variable')
    plt.ylabel('Average in Years')
    plt.legend()
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.show()


########################


    # Create a crosstab of Attrition and OverTime
    crosstab_df = pd.crosstab(attrition_df['Attrition'], attrition_df['OverTime'])

    # Plot the stacked bar chart
    crosstab_df.plot.bar(stacked=True)

    # Set the title and axis labels
    plt.title('Attrition by Overtime',fontsize=16)
    plt.xlabel('Attrition',fontsize=16)
    plt.ylabel('Employee Count',fontsize=16)

    # Show the plot
    plt.show()


########################

    plt.figure(figsize=(20,6))

    sns.kdeplot(x=attrition_df.loc[attrition_df['Attrition'] == 'No', 'Age'], label = 'Active Employee', color="g")
    sns.kdeplot(x=attrition_df.loc[attrition_df['Attrition'] == 'Yes', 'Age'], label = 'Active Employee', color="b")
    plt.xlim(left=18, right=60)
    plt.legend(["Stay","Left"])
    plt.show()


########################


    # Create two dataframes for attrition yes and no
    attrition_yes_df = attrition_df[attrition_df['Attrition'] == 'Yes']
    attrition_no_df = attrition_df[attrition_df['Attrition'] == 'No']

    # Define a dictionary to map the job satisfaction levels to their values
    job_satisfaction_dict = {
        1: 'Low',
        2: 'Medium',
        3: 'High',
        4: 'Very High'
    }

    job_satisfaction_colors = {
        'Low': 'red',
        'Medium': 'orange',
        'High': 'blue',
        'Very High': 'green'
    }

    # Replace the job satisfaction levels with their values in both dataframes
    attrition_df['JobSatisfaction'] = attrition_df['JobSatisfaction'].replace(job_satisfaction_dict)
    attrition_yes_df['JobSatisfaction'] = attrition_yes_df['JobSatisfaction'].replace(job_satisfaction_dict)
    attrition_no_df['JobSatisfaction'] = attrition_no_df['JobSatisfaction'].replace(job_satisfaction_dict)

    # Create a pie chart for attrition yes and job satisfaction with colors
    attrition_yes_job_satisfaction = attrition_yes_df['JobSatisfaction'].value_counts()
    plt.pie(attrition_yes_job_satisfaction,
            labels=attrition_yes_job_satisfaction.index,
            colors=[job_satisfaction_colors[x] for x in attrition_yes_job_satisfaction.index],
            autopct='%1.1f%%')
    plt.title('Attrition Yes: Job Satisfaction')
    plt.show()

    # Create a pie chart for attrition no and job satisfaction with colors
    attrition_no_job_satisfaction = attrition_no_df['JobSatisfaction'].value_counts()
    plt.pie(attrition_no_job_satisfaction,
            labels=attrition_no_job_satisfaction.index,
            colors=[job_satisfaction_colors[x] for x in attrition_no_job_satisfaction.index],
            autopct='%1.1f%%')
    plt.title('Attrition No: Job Satisfaction')
    plt.show()


########################
    # Define a dictionary to map the job satisfaction levels to their values
    education_dict = {
        1: 'Below College',
        2: 'College',
        3: 'Bachelor',
        4: 'Master',
        5: 'Doctor'
    }
    attrition_df['Education'] = attrition_df['Education'].replace(education_dict)

    # Group the data by education field and attrition status
    edu_attrition_counts = attrition_df.groupby(['Education', 'Attrition']).size().unstack()

    # Create a bar chart
    edu_attrition_counts.plot(kind='bar', stacked=True, color=['#4c78a8', '#f58518'])

    # Set the labels and title
    plt.xlabel('Education Level')
    plt.ylabel('Count')
    plt.title('Employee Attrition by Educational Level')
    plt.xticks(rotation=0)

    # Show the plot
    plt.show()

########################
    sns.countplot(x='BusinessTravel', palette="Set3", hue='Attrition', data=attrition_df)
    plt.show()


if __name__ == '__main__':
    attrition_df = fetch_data()
    create_plots(attrition_df)
    create_plot_coeff(coef_df)

