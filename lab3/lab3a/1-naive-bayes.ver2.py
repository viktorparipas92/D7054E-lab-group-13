import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.model_selection import learning_curve
import numpy as np


def create_model(features, labels):
    (
        features_train,
        features_test,
        labels_train,
        labels_test,
    ) = train_test_split(features, labels, random_state=23)

    naive_bayes_model = GaussianNB()
    naive_bayes_model.fit(features_train, labels_train)

    pred_labels = naive_bayes_model.predict(features_test)

    return labels_test, pred_labels


def get_metrics(labels_test, pred_labels):
    cm = metrics.confusion_matrix(labels_test, pred_labels)
    print(cm)

    report = classification_report(labels_test, pred_labels)
    print(report)

    sns.heatmap(cm, annot=True, cmap='YlGnBu', fmt='g', annot_kws={"fontsize": 18})

    plt.xlabel('Predicted label', fontsize=20)
    plt.ylabel('True label', fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('Confusion Matrix', fontsize=20)
    plt.show()


def learn_curve(features, labels):
    # Compute the learning curve scores
    train_sizes, train_scores, test_scores = learning_curve(
        GaussianNB(),
        features,
        labels,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        train_sizes=[0.1, 0.3, 0.5, 0.7, 0.9]
    )
    # Plot the learning curve
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color="r", label="Training score")
    plt.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color="g", label="Cross-validation score")
    plt.legend(loc="best", fontsize=20)
    plt.xlabel("Training examples", fontsize=20)
    plt.ylabel("Accuracy score", fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('Learning Curve (Naive Bayes Classifier)', fontsize=16)
    plt.tight_layout()

    plt.show()


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

    wine_labels_test, predicted_labels = create_model(wine_features, wine_labels)
    get_metrics(wine_labels_test, predicted_labels)
    learn_curve(wine_features, wine_labels)
