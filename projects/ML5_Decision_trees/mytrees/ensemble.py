import numpy as np
from concurrent.futures import ProcessPoolExecutor

from .tree import MyDecisionTreeClassifier, MyDecisionTreeRegressor


def _fit_one_tree(args):
    X, y, params, seed, max_features, classes = args
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(y), len(y), replace=True) if not params["ERT"] else np.arange(len(y))
    columns_idx = rng.choice(X.shape[1], max_features, replace=False) if not params["ERT"] else np.arange(X.shape[1])

    mf = max_features if params["ERT"] else None
    tree = MyDecisionTreeClassifier(**params, max_features=mf)
    tree.fit(X[idx][:, columns_idx], y[idx], classes)
    return (tree, columns_idx)


class MyRandomForestClassifier:
    def __init__(self, n_estimators: int, max_depth: int, max_features: int | None = None, n_jobs = 1, seed: int | None = None, ETC: bool = False) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.seed = seed
        self.n_jobs = n_jobs
        self.trees = None
        self.ETC = ETC

    def fit(self, X, y):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        y = y.to_numpy() if hasattr(y, "to_numpy") else y
        self.classes = np.unique(y)

        max_features = min(self.max_features, X.shape[1]) if self.max_features else int(np.sqrt(X.shape[1]))
        ss = np.random.SeedSequence(self.seed)
        child_seeds = ss.spawn(self.n_estimators)
        params = {"max_depth": self.max_depth, "ERT": self.ETC,}


        args_list = [(X, y, params, seed, max_features, self.classes) for seed in child_seeds]
        with ProcessPoolExecutor(max_workers=self.n_jobs) as ex:
            self.trees = list(ex.map(_fit_one_tree, args_list))

    def predict_proba(self, X):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        if not self.trees:
            print("Model is not trained yet")
            return None

        probs = np.mean(
            np.array([tree.predict_proba(X[:, columns_idx]) for tree, columns_idx in self.trees]),
            axis=0
        )
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        idx = np.argmax(probs, axis=1)
        return self.classes[idx]


class MyGradientBoostingClassifier:
    def __init__(
            self, max_depth: int,
            number_of_trees: int,
            max_features: int | None = None,
            learning_rate: float = 0.01,
            seed: int | None = None
            ) -> None:
        self.max_depth = max_depth
        self.number_of_trees = number_of_trees
        self.max_features = max_features
        self.learning_rate = learning_rate
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.trees = []

    def sigmoid(self, values):
        return 1 / (1 + np.exp(-values))

    def loss_antigradient(self, y_true, y_pred):
        return y_true - self.sigmoid(y_pred)

    def fit(self, X, y):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        y_mean = np.mean(y, axis=0)
        self.y_base = np.log(y_mean / (1 - y_mean))
        y_pred = np.full(y.shape, self.y_base)
        max_features = min(self.max_features, X.shape[1]) if self.max_features else int(np.sqrt(X.shape[1]))

        for _ in range(self.number_of_trees):
            gradient = self.loss_antigradient(y, y_pred)
            columns_idx = self.rng.choice(X.shape[1], max_features, replace=False)
            tree = MyDecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X[:, columns_idx], gradient)

            self.trees.append((tree, columns_idx))
            y_pred += self.learning_rate * tree.predict(X[:, columns_idx])

    def predict_proba(self, X):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        if not self.trees:
            print("Model is not trained yet")
            return None

        predictions = np.sum(
            [
                tree.predict(X[:, columns]) for tree, columns in self.trees
            ],
            axis=0
        )
        return self.sigmoid(self.y_base + self.learning_rate * predictions)

    def predict(self, X):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        return (self.predict_proba(X) >= 0.5).astype(int)
