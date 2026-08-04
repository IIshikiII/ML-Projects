import numpy as np
from collections import deque
from concurrent.futures import ThreadPoolExecutor

from ._nodes import MyNode, MyNodeRegressor


class MyDecisionTreeClassifier:
    def __init__(self, max_depth=10, verbose=False, ERT=False, n_jobs=1, max_features=None) -> None:
        self.max_depth = max_depth
        self.root = None
        self.verbose = verbose
        self.ERT = ERT
        self.njobs=n_jobs
        self.max_features = max_features

    def fit(self, X, y, classes=None):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        core_node = MyNode(X, y, max_depth=self.max_depth, verbose = self.verbose, ERT=self.ERT, classes=classes, max_features=self.max_features)
        self.root = core_node

        if self.njobs <= 1:
            nodes = deque([core_node])


            while nodes:
                node = nodes.popleft()
                if not node or node.stop:
                    continue
                node.step()
                nodes.append(node.childl)
                nodes.append(node.childr)
            return

        with ThreadPoolExecutor(max_workers=self.njobs) as executor:
            current_level = [core_node]
            while current_level:
                active_nodes = [n for n in current_level if n is not None and not n.stop]
                if not active_nodes:
                    break

                if len(active_nodes) == 1:
                    active_nodes[0].step(executor=executor)
                else:
                    list(executor.map(lambda n: n.step(), active_nodes))

                next_level=[]
                for node in active_nodes:
                    next_level.append(node.childl)
                    next_level.append(node.childr)
                current_level = next_level

    def predict_proba(self, X):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        if not self.root:
            print("Model is not trained yet")
            return None

        nodes = [[self.root, self.root.stop] for _ in range(len(X))]
        while any(not item[1] for item in nodes):
            for i, node in enumerate(nodes):
                if not node[1]:
                    col = node[0].best_threshold["column"]
                    thr = node[0].best_threshold["row"]
                    if X[i, col] <= thr:
                        node[0] = node[0].childl
                    else:
                        node[0] = node[0].childr
                    node[1] = node[0].stop


        return np.array([node[0].class_probs for node in nodes])

    def predict(self, X):
        proba = self.predict_proba(X)
        idx = np.argmax(proba, axis=1)
        return self.root.classes[idx]


class MyDecisionTreeRegressor:
    def __init__(self, max_depth=10, verbose=False, ERT=False, seed=None) -> None:
        self.max_depth = max_depth
        self.root = None
        self.verbose = verbose
        self.ERT = ERT
        self.seed = seed

    def fit(self, X, y):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        core_node = MyNodeRegressor(X, y, max_depth=self.max_depth, verbose=self.verbose, ERT=self.ERT, seed=self.seed)
        self.root = core_node
        nodes = deque([core_node])

        while nodes:
            node = nodes.popleft()
            if not node or node.stop:
                continue
            node.step()
            nodes.append(node.childl)
            nodes.append(node.childr)

    def predict(self, X):
        X = X.to_numpy() if hasattr(X, "to_numpy") else X
        if not self.root:
            print("Model is not trained yet")
            return None

        nodes = [[self.root, self.root.stop] for _ in range(len(X))]
        while any(not item[1] for item in nodes):
            for i, node in enumerate(nodes):
                if not node[1]:
                    col = node[0].best_threshold["column"]
                    thr = node[0].best_threshold["row"]
                    if X[i, col] <= thr:
                        node[0] = node[0].childl
                    else:
                        node[0] = node[0].childr
                    node[1] = node[0].stop

        return np.array([node[0].value for node in nodes])
