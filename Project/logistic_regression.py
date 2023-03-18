from imblearn.over_sampling import SMOTE
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from attrition_api import fetch_data
from dataset import preprocess_attrition_data


def get_coefficient_dataframe(model, features):
    coefficients = model.coef_[0]
    coefficient_df = pd.DataFrame(
        {'feature': features.columns.tolist(), 'coefficient': coefficients}
    )
    coefficient_df = coefficient_df.sort_values(
        by='coefficient', ascending=False
    )
    return coefficient_df


def train_logistic_regression(df):
    x, y = preprocess_attrition_data(df)

    # Oversample the minority class
    smote = SMOTE()
    x, y = smote.fit_resample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=23
    )
    logistic_regression = LogisticRegression(
        solver='lbfgs', max_iter=4500, class_weight='balanced'
    )
    logistic_regression.fit(x_train, y_train)
    y_predicted = logistic_regression.predict(x_test)

    accuracy = logistic_regression.score(x_test, y_test)
    cr = classification_report(y_test, y_predicted)
    print(cr)

    coefficient_dataframe = get_coefficient_dataframe(logistic_regression, x)

    return logistic_regression, y_predicted, accuracy, coefficient_dataframe


def create_plot_coefficients(coef_df):
    plt.xlabel('Coefficient Value')
    plt.ylabel('Feature')
    plt.yticks([])
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
