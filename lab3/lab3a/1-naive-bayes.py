import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


if __name__ == '__main__':
    column_names = [
        'Class',
        'Alcohol',
        'Malic acid',
        'Ash',
        'Alcalinity of ash',
        'Magnesium',
        'Total phenols',
        'Flavanoids',
        'Nonflavanoid phenols',
        'Proanthocyanins',
        'Color intensity',
        'Hue',
        'OD280/OD315 of diluted wines',
        'Proline',
    ]

    wine_data = pd.read_csv('../datasets/wine.csv', names=column_names)
    wine_labels = wine_data['Class']
    wine_features = wine_data.drop(columns=['Class'])
    (
        wine_features_train,
        wine_features_test,
        wine_labels_train,
        wine_labels_test,
    ) = train_test_split(wine_features, wine_labels, random_state=23)

    naive_bayes_model = GaussianNB()
    naive_bayes_model.fit(wine_features_train, wine_labels_train)

    predicted_labels = naive_bayes_model.predict(wine_features_test)
    print(f"Accuracy: {accuracy_score(wine_labels_test, predicted_labels):.3f}")
