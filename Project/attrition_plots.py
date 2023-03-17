import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


FONT_SIZE = 16


def create_hist_age_distribution(data):
    attrition_yes: pd.DataFrame = data[data['Attrition'] == 'Yes']['Age']
    attrition_no: pd.DataFrame = data[data['Attrition'] == 'No']['Age']
    plt.hist(
        [attrition_yes, attrition_no],
        bins=30,
        color=['red', 'blue'],
        label=['Attrition: Yes', 'Attrition: No'],
    )
    plt.xlabel('Age', fontsize=FONT_SIZE)
    plt.ylabel('Count', fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.title('Age Distribution by Attrition Status')
    plt.legend()
    plt.show()


def create_violinplot(data):
    sns.violinplot(
        x='Attrition',
        y='YearsAtCompany',
        fontsize=FONT_SIZE,
        hue='Gender',
        data=data,
        split=True,
    )
    plt.title('Years at Company Distribution by Attrition and Gender')
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.show()


def create_stacked_bar_average_years(data):
    attrition_means = data.groupby('Attrition')[
        ['YearsAtCompany', 'TotalWorkingYears', 'YearsSinceLastPromotion']
    ].mean()
    plt.bar(attrition_means.columns, attrition_means.loc['No'], label='No')
    plt.bar(
        attrition_means.columns,
        attrition_means.loc['Yes'],
        bottom=attrition_means.loc['No'],
        label='Yes',
    )
    plt.title('Attrition')
    plt.xlabel('Variable')
    plt.ylabel('Average in Years')
    plt.legend(fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.show()


def create_bar_overtime(data: pd.DataFrame):
    crosstab_data: pd.DataFrame = pd.crosstab(
        data['Attrition'], data['OverTime']
    )
    crosstab_data.plot.bar(stacked=True)
    plt.title('Attrition by Overtime', fontsize=FONT_SIZE)
    plt.xlabel('Attrition', fontsize=FONT_SIZE)
    plt.ylabel('Employee Count', fontsize=FONT_SIZE)
    plt.legend(fontsize=FONT_SIZE)
    plt.xticks(rotation=0, fontsize=FONT_SIZE)
    plt.show()


def create_pie_charts(data):
    attrition_yes: pd.DataFrame = data[data['Attrition'] == 'Yes']
    attrition_no: pd.DataFrame = data[data['Attrition'] == 'No']
    job_satisfaction_levels: dict = {
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

    data['JobSatisfaction'] = data['JobSatisfaction'].replace(
        job_satisfaction_levels
    )
    attrition_yes = attrition_yes.copy()
    attrition_yes.loc[:, 'JobSatisfaction'] = attrition_yes[
        'JobSatisfaction'
    ].replace(job_satisfaction_levels)
    attrition_yes_job_satisfaction = attrition_yes[
        'JobSatisfaction'
    ].value_counts()
    plt.pie(
        attrition_yes_job_satisfaction,
        labels=attrition_yes_job_satisfaction.index,
        colors=[
            job_satisfaction_colors[job_satisfaction_level]
            for job_satisfaction_level in attrition_yes_job_satisfaction.index
        ],
        autopct='%1.1f%%',
        textprops={'fontsize': FONT_SIZE},
    )
    plt.title('Attrition Yes: Job Satisfaction')
    plt.show()

    attrition_no = attrition_no.copy()
    attrition_no.loc[:, 'JobSatisfaction'] = attrition_no[
        'JobSatisfaction'
    ].replace(job_satisfaction_levels)
    attrition_no_job_satisfaction = attrition_no[
        'JobSatisfaction'
    ].value_counts()
    plt.pie(
        attrition_no_job_satisfaction,
        labels=attrition_no_job_satisfaction.index,
        colors=[
            job_satisfaction_colors[x]
            for x in attrition_no_job_satisfaction.index
        ],
        autopct='%1.1f%%',
        textprops={'fontsize': FONT_SIZE})
    plt.title('Attrition No: Job Satisfaction')
    plt.show()


def create_bar_education_level(data: pd.DataFrame):
    education_levels: dict = {
        1: 'Below College',
        2: 'College',
        3: 'Bachelor',
        4: 'Master',
        5: 'Doctor'
    }
    data['Education'] = data['Education'].replace(education_levels)
    data['Education'] = pd.Categorical(
        data['Education'],
        ordered=True,
        categories=list(education_levels.values())
    )
    data.sort_values(by='Education', inplace=True)
    education_level_attrition_counts = data.groupby(
        ['Education', 'Attrition']
    ).size().unstack()
    education_level_attrition_counts.plot(
        kind='bar', stacked=True, color=['#4c78a8', '#f58518']
    )
    plt.xlabel('Education Level', fontsize=FONT_SIZE)
    plt.ylabel('Count', fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.title('Employee Attrition by Educational Level')
    plt.xticks(rotation=0)
    plt.legend(fontsize=FONT_SIZE)
    plt.show()


def create_plot_business_travel(data: pd.DataFrame):
    sns.set(font_scale=1.5)
    sns.countplot(
        x='BusinessTravel',
        palette='Set2',
        hue='Attrition',
        data=data,
        order=['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']
    )
    plt.show()
