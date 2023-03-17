import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def create_hist_age_distribution(data):
    attrition_yes = data[data['Attrition'] == 'Yes']['Age']
    attrition_no = data[data['Attrition'] == 'No']['Age']
    plt.hist(
        [attrition_yes, attrition_no],
        bins=30,
        color=['red', 'blue'],
        label=['Attrition: Yes', 'Attrition: No'],
    )
    plt.xlabel('Age', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Age Distribution by Attrition Status')
    plt.legend()
    plt.show()


def create_violinplot(data):
    sns.violinplot(
        x='Attrition',
        y='YearsAtCompany',
        fontsize=16,
        hue='Gender',
        data=data,
        split=True,
    )
    plt.title('Years at Company Distribution by Attrition and Gender')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
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
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.show()


def create_bar_overtime(data):
    crosstab_df = pd.crosstab(data['Attrition'], data['OverTime'])
    crosstab_df.plot.bar(stacked=True)
    plt.title('Attrition by Overtime', fontsize=16)
    plt.xlabel('Attrition', fontsize=16)
    plt.ylabel('Employee Count', fontsize=16)
    plt.legend(fontsize=16)
    plt.xticks(rotation=0, fontsize=16)
    plt.show()


def create_pie_charts(data):
    attrition_yes_df = data[data['Attrition'] == 'Yes']
    attrition_no_df = data[data['Attrition'] == 'No']
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

    data['JobSatisfaction'] = data['JobSatisfaction'].replace(
        job_satisfaction_dict
    )
    attrition_yes_df = attrition_yes_df.copy()
    attrition_yes_df.loc[:, 'JobSatisfaction'] = attrition_yes_df[
        'JobSatisfaction'
    ].replace(job_satisfaction_dict)
    attrition_no_df = attrition_no_df.copy()
    attrition_no_df.loc[:, 'JobSatisfaction'] = attrition_no_df[
        'JobSatisfaction'
    ].replace(job_satisfaction_dict)
    attrition_yes_job_satisfaction = attrition_yes_df[
        'JobSatisfaction'
    ].value_counts()
    plt.pie(
        attrition_yes_job_satisfaction,
        labels=attrition_yes_job_satisfaction.index,
        colors=[
            job_satisfaction_colors[x]
            for x in attrition_yes_job_satisfaction.index
        ],
        autopct='%1.1f%%',
        textprops={'fontsize': 16},
    )
    plt.title('Attrition Yes: Job Satisfaction')
    plt.show()
    attrition_no_job_satisfaction = attrition_no_df[
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
        textprops={'fontsize': 16})
    plt.title('Attrition No: Job Satisfaction')
    plt.show()


def create_bar_education_level(data):
    education_dict = {
        1: 'Below College',
        2: 'College',
        3: 'Bachelor',
        4: 'Master',
        5: 'Doctor'
    }
    data['Education'] = data['Education'].replace(education_dict)
    data['Education'] = pd.Categorical(
        data['Education'],
        ordered=True,
        categories=[education_dict[i] for i in sorted(education_dict.keys())]
    )
    data.sort_values(by='Education', inplace=True)
    edu_attrition_counts = data.groupby(
        ['Education', 'Attrition']
    ).size().unstack()
    edu_attrition_counts.plot(
        kind='bar', stacked=True, color=['#4c78a8', '#f58518']
    )
    plt.xlabel('Education Level', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Employee Attrition by Educational Level')
    plt.xticks(rotation=0)
    plt.legend(fontsize=16)
    plt.show()


def create_plot_business_travel(data):
    sns.set(font_scale=1.5)
    sns.countplot(
        x='BusinessTravel',
        palette='Set2',
        hue='Attrition',
        data=data,
        order=['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']
    )
    plt.show()
