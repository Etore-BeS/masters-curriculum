from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = Path(__file__).with_name("liver.csv")
TARGET = "heavy_drinker"
FEATURES = ["mcv", "alkphos", "sgpt", "sgot", "gammagt"]
SEEDS = [42, 7, 13, 21, 99]
TEST_SIZE = 0.3


def load_data(path: Path = DATA_PATH):
    data = pd.read_csv(path)
    features = data[FEATURES]
    labels = data[TARGET]
    return features, labels


def majority_vote(predictions):
    stacked = np.column_stack(predictions)
    return np.apply_along_axis(
        lambda row: np.bincount(row.astype(int)).argmax(),
        axis=1,
        arr=stacked,
    )


def run_repetition(features, labels, seed: int):
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=TEST_SIZE,
        random_state=seed,
        stratify=labels,
    )
    tree = DecisionTreeClassifier(criterion="entropy", random_state=0)
    naive_bayes = GaussianNB()
    knn = KNeighborsClassifier(n_neighbors=5)
    for classifier in (tree, naive_bayes, knn):
        classifier.fit(x_train, y_train)

    tree_pred = tree.predict(x_test)
    nb_pred = naive_bayes.predict(x_test)
    knn_pred = knn.predict(x_test)
    ensemble_pred = majority_vote([tree_pred, nb_pred, knn_pred])

    return {
        "seed": seed,
        "tree": 1.0 - accuracy_score(y_test, tree_pred),
        "nb": 1.0 - accuracy_score(y_test, nb_pred),
        "knn": 1.0 - accuracy_score(y_test, knn_pred),
        "ensemble": 1.0 - accuracy_score(y_test, ensemble_pred),
        "n_train": len(x_train),
        "n_test": len(x_test),
    }


def run_experiments(features=None, labels=None, seeds=SEEDS):
    if features is None or labels is None:
        features, labels = load_data()
    rows = [run_repetition(features, labels, seed) for seed in seeds]
    results = pd.DataFrame(rows)
    means = results.drop(columns=["seed", "n_train", "n_test"]).mean()
    return results, means
