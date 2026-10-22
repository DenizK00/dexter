import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, roc_curve, auc, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from hyperopt import hp, fmin, tpe, space_eval

MODELS = {
    "logistic_regression": LogisticRegression,
    "k_neighbors": KNeighborsClassifier,
    "SVC": SVC,
    "random_forest": RandomForestClassifier,
    "gradient_boosting": GradientBoostingClassifier,
}

MODE_TO_MODELS = {
    "standard": ["logistic_regression", "k_neighbors", "SVC"],
    "extensive": list(MODELS),
}

PARAM_SPACES = {
    "logistic_regression": {"C": hp.loguniform("C", np.log(0.1), np.log(100)), "penalty": hp.choice("penalty", ["l1", "l2"]), "solver": hp.choice("solver", ["liblinear", "saga"]), "max_iter": hp.choice("max_iter", [1000])},
    "SVC": {"C": hp.loguniform("C", np.log(0.1), np.log(100)), "gamma": hp.choice("gamma", [0.1, 1, 10, "auto"]), "kernel": hp.choice("kernel", ["linear", "rbf", "poly"]), "degree": hp.choice("degree", [2, 3, 4])},
    "k_neighbors": {"n_neighbors": hp.choice("n_neighbors", list(range(1, 10)))},
    "random_forest": {"n_estimators": hp.choice("n_estimators", [50, 100, 200, 400]), "max_depth": hp.choice("max_depth", [None, 3, 5, 10, 20])},
    "gradient_boosting": {"n_estimators": hp.choice("n_estimators", [50, 100, 200]), "learning_rate": hp.loguniform("learning_rate", np.log(0.01), np.log(0.5)), "max_depth": hp.choice("max_depth", [2, 3, 5])},
}


def pick_classifier(df: pd.DataFrame, target: str, features=None, test_size=0.2, visualize=False, mode="standard", decimals=4, fold_count=6, random_state=None, choice=None, max_evals=100):
    """Finds the best classifier.

    Compares the models of ``mode`` on a train/test split, then tunes the
    chosen one with hyperopt. Pass ``choice`` (a key of ``MODELS``) to skip the
    interactive prompt.
    """

    X = df[features].values if features else df.drop(target, axis=1).values
    y = df[target].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    kf = KFold(n_splits=fold_count, random_state=random_state, shuffle=True)

    binary = np.unique(y).size <= 2
    scoring = "roc_auc" if binary else "f1_weighted"
    print("Binary Classification" if binary else "Multiclass Classification")

    models = {name: MODELS[name]() for name in MODE_TO_MODELS[mode]}

    accuracy_scores, f1_scores, cv_results = [], [], []

    for model in models.values():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy_scores.append(str(round(accuracy_score(y_test, y_pred), decimals)))
        f1_scores.append(str(round(f1_score(y_test, y_pred, average='weighted'), decimals)))
        cv_results.append(str(round(cross_val_score(model, X_train, y_train, cv=kf, scoring=scoring).mean(), decimals)))

    print(f"Model:           {' '.join(models.keys())}")
    print(f"Cross Val Score {' '.join(cv_results)}")
    print(f"Accuracy Score:  {' '.join(accuracy_scores)}")
    print(f"F1 Score:        {' '.join(f1_scores)}")

    if choice is None:
        choice = input("Which model to proceed?")
        while choice not in models:
            print("Please choose from the following", " ".join(models.keys()))
            choice = input("Which model to proceed?")
    elif choice not in models:
        raise ValueError(f"choice must be one of {list(models)}")
    print(f"\nChosen {choice}")

    chosen_model = models[choice]
    space = PARAM_SPACES[choice]

    def objective(params):
        clf = chosen_model.set_params(**params)
        return 1 - cross_val_score(clf, X_train, y_train, cv=kf, scoring=scoring).mean()

    best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=max_evals)
    best_params = space_eval(space, best)

    chosen_model = chosen_model.set_params(**best_params)
    chosen_model.fit(X_train, y_train)

    print(f"Tuned {choice} parameters: {best_params}")
    print(f"Tuned {choice} test score: {round(chosen_model.score(X_test, y_test), decimals)}")

    if visualize:
        _plot_results(chosen_model, X_test, y_test, binary)

    return chosen_model


def _plot_results(model, X_test, y_test, binary):
    import matplotlib.pyplot as plt
    import seaborn as sns

    test_pred = model.predict(X_test)
    labels = np.unique(y_test)
    fig, axes = plt.subplots(1, 2 if binary else 1, figsize=(12, 5), squeeze=False)
    axes = axes[0]

    cm = confusion_matrix(y_test, test_pred, labels=labels)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
        xticklabels=[f"Predicted {label}" for label in labels],
        yticklabels=[f"Actual {label}" for label in labels], ax=axes[0])

    if binary:
        if hasattr(model, "predict_proba"):
            test_scores = model.predict_proba(X_test)[:, 1]
        else:
            test_scores = model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, test_scores, pos_label=labels[-1])
        roc_auc = auc(fpr, tpr)

        sns.lineplot(x=fpr, y=tpr, color='darkorange', label='ROC curve (AUC = {:.2f})'.format(roc_auc), ax=axes[1])
        sns.lineplot(x=[0, 1], y=[0, 1], color='navy', linestyle='--', label='Random Guess', ax=axes[1])

        axes[1].set_xlim([0.0, 1.0])
        axes[1].set_ylim([0.0, 1.05])
        axes[1].set_xlabel("False Positive Rate")
        axes[1].set_ylabel("True Positive Rate")
        axes[1].set_title("ROC Curve")
        axes[1].legend(loc="lower right")

    if hasattr(model, "coef_"):
        print(model.coef_)

    plt.show()
