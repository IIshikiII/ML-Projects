import numpy as np


class MyNode:
    def __init__(self, X, y, stop=False, max_depth=10, curr_depth=0, classes=None, verbose=False, ERT=False, seed = None, max_features=None):
        self.X = X
        self.y = y
        self.childl = None
        self.childr = None
        self.stop = stop
        self.verbose = verbose
        self.ERT = ERT
        self.max_features = max_features

        self.max_depth = max_depth
        self.curr_depth = curr_depth

        self.classes = classes if classes is not None else np.unique(y)
        self.rng = np.random.default_rng(seed=seed)

        if self.curr_depth >= self.max_depth:
            self.stop = True

        self.gini = self.calc_gini(self.y)
        if not self.stop and self.gini == 0:
            self.stop = True

        self.best_threshold = None
        self.best_Q = 0.0


        counts = np.array([(y == c).sum() for c in self.classes], dtype=np.float64)
        self.class_probs = counts / len(y)

    def calc_gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1 - np.sum(probs ** 2)

    def _best_split_for_column(self, x_col, y):
        order = np.argsort(x_col, kind="mergesort")
        x_sorted = x_col[order]
        y_sorted = y[order]

        n = len(y)
        classes = self.classes
        k = len(classes)

        y_onehot = (y_sorted[:, None] == classes[None, :]).astype(np.float64)
        cum_left = np.cumsum(y_onehot, axis=0)
        total = cum_left[-1]
        cum_right = total - cum_left

        n_left = np.arange(1, n + 1, dtype=np.float64)
        n_right = n - n_left

        valid_len = n - 1
        if valid_len <= 0:
            return None

        n_left = n_left[:valid_len]
        n_right = n_right[:valid_len]
        cum_left = cum_left[:valid_len]
        cum_right = cum_right[:valid_len]

        valid = x_sorted[:-1] != x_sorted[1:]
        if not valid.any():
            return None

        if self.verbose:
            print(cum_left)
            print(cum_right)

        gini_left = 1 - np.sum((cum_left / n_left[:, None]) ** 2, axis=1)
        gini_right = 1 - np.sum((cum_right / n_right[:, None]) ** 2, axis=1)

        mgini = self.gini
        Q = mgini - (n_left / n) * gini_left - (n_right / n) * gini_right
        Q = np.where(valid, Q, -np.inf)

        best_i = np.argmax(Q)
        if not np.isfinite(Q[best_i]) or Q[best_i] <= 0:
            return None

        threshold = (x_sorted[best_i] + x_sorted[best_i + 1]) / 2.0
        left_mask = x_col <= threshold

        return {
            "Q": Q[best_i],
            "threshold": threshold,
            "left_mask": left_mask,
            "lgini": gini_left[best_i],
            "rgini": gini_right[best_i],
        }

    def _ERT_split_for_column(self, x_col, y, rng=None):
        rng = rng if rng is not None else self.rng
        lo, hi = x_col.min(), x_col.max()
        if lo == hi:
            return None

        thr = rng.uniform(lo, hi)
        left = x_col <= thr
        nl = left.sum(); nr = len(y) - nl
        if nl == 0 or nr == 0:
            return None
        yl, yr = y[left], y[~left]
        gl = self.calc_gini(yl)
        gr = self.calc_gini(yr)
        Q = self.gini - (nl/len(y))*gl - (nr/len(y))*gr
        return {"Q": Q, "threshold": thr, "left_mask": left, "lgini": gl, "rgini": gr}

    def find_optimal_split(self, executor=None):
        if self.stop:
            self.best_threshold = None
            return None

        best = None
        best_column = None

        if self.ERT:
            p = self.X.shape[1]
            n_feat = min(self.max_features, p) if self.max_features is not None else int(np.sqrt(p))
            columns_to_check = self.rng.choice(self.X.shape[1], n_feat, replace=False)
        else:
            columns_to_check = range(self.X.shape[1])

        if executor:
            if self.ERT:
                child_rngs = self.rng.spawn(len(columns_to_check))
                results = list(executor.map(
                    lambda args: self._ERT_split_for_column(self.X[:, args[0]], self.y, rng=args[1]),
                    zip(columns_to_check, child_rngs)
                ))
            else:
                results = list(executor.map(
                    lambda column: self._best_split_for_column(self.X[:, column], self.y),
                    columns_to_check
                ))
            for column, result in zip(columns_to_check, results):
                if result is None:
                    continue
                if best is None or result["Q"] > best["Q"]:
                    best = result
                    best_column = column
        else:
            for column in columns_to_check:
                if self.ERT:
                    result = self._ERT_split_for_column(self.X[:, column], self.y)
                else:
                    result = self._best_split_for_column(self.X[:, column], self.y)

                if result is None:
                    continue
                if best is None or result["Q"] > best["Q"]:
                    best = result
                    best_column = column

        if best is None:
            self.best_threshold = None
            return None

        left_mask = best["left_mask"]
        right_mask = ~left_mask

        self.best_Q = best["Q"]
        self.best_threshold = {
            "column": best_column,
            "row": best["threshold"],
            "left_mask": left_mask,
            "right_mask": right_mask,
            "lgini": best["lgini"],
            "rgini": best["rgini"],
        }
        return self.best_threshold

    def step(self, executor=None):
        self.find_optimal_split(executor=executor)

        if self.best_threshold is None:
            self.stop = True
            return None

        left_mask = self.best_threshold["left_mask"]
        right_mask = self.best_threshold["right_mask"]

        childl_stop = self.best_threshold["lgini"] == 0
        childr_stop = self.best_threshold["rgini"] == 0

        self.childl = MyNode(
            self.X[left_mask],
            self.y[left_mask],
            stop=childl_stop,
            curr_depth=self.curr_depth + 1,
            max_depth=self.max_depth,
            classes=self.classes,
            ERT=self.ERT,
            verbose=self.verbose,
            max_features=self.max_features
        )
        self.childr = MyNode(
            self.X[right_mask],
            self.y[right_mask],
            stop=childr_stop,
            curr_depth=self.curr_depth + 1,
            max_depth=self.max_depth,
            classes=self.classes,
            ERT=self.ERT,
            verbose=self.verbose,
            max_features=self.max_features
        )
        return self.best_threshold


class MyNodeRegressor:
    def __init__(self, X, y, stop=False, max_depth=10, curr_depth=0, verbose=False, ERT=False, seed = None, rng = None):
        self.X = X
        self.y = y
        self.childl = None
        self.childr = None
        self.stop = stop
        self.verbose = verbose
        self.ERT = ERT
        self.rng = rng if rng else np.random.default_rng(seed=seed)

        self.max_depth = max_depth
        self.curr_depth = curr_depth

        if self.curr_depth >= self.max_depth:
            self.stop = True

        self.std = self.calc_std(self.y)
        if not self.stop and self.std == 0:
            self.stop = True

        self.best_threshold = None
        self.best_Q = 0.0

        self.value = np.mean(y)

    def calc_std(self, y):
        return np.std(y)

    def _best_split_for_column(self, x_col, y):
        order = np.argsort(x_col, kind="mergesort")
        x_sorted = x_col[order]
        y_sorted = y[order]

        n = len(y)

        cum_sum = np.cumsum(y_sorted)
        cum_sq = np.cumsum(y_sorted ** 2)
        total_sum = cum_sum[-1]
        total_sq = cum_sq[-1]

        n_left = np.arange(1, n + 1, dtype=np.float64)
        n_right = n - n_left

        valid_len = n - 1
        if valid_len <= 0:
            return None

        n_left = n_left[:valid_len]
        n_right = n_right[:valid_len]
        cum_sum = cum_sum[:valid_len]
        cum_sq = cum_sq[:valid_len]

        valid = x_sorted[:-1] != x_sorted[1:]
        if not valid.any():
            return None

        mean_left = cum_sum / n_left
        var_left = np.maximum(cum_sq / n_left - mean_left ** 2, 0)
        std_left = np.sqrt(var_left)

        sum_right = total_sum - cum_sum
        sq_right = total_sq - cum_sq
        mean_right = sum_right / n_right
        var_right = np.maximum(sq_right / n_right - mean_right ** 2, 0)
        std_right = np.sqrt(var_right)

        m_std = self.std
        Q = m_std - (n_left / n) * std_left - (n_right / n) * std_right
        Q = np.where(valid, Q, -np.inf)

        best_i = np.argmax(Q)
        if not np.isfinite(Q[best_i]) or Q[best_i] <= 0:
            return None

        threshold = (x_sorted[best_i] + x_sorted[best_i + 1]) / 2.0
        left_mask = x_col <= threshold

        return {
            "Q": Q[best_i],
            "threshold": threshold,
            "left_mask": left_mask,
            "lstd": std_left[best_i],
            "rstd": std_right[best_i],
        }

    def _ERT_split_for_column(self, x_col, y, rng=None):
        rng = rng if rng is not None else self.rng
        lo, hi = x_col.min(), x_col.max()
        if lo == hi:
            return None

        thr = rng.uniform(lo, hi)
        left = x_col <= thr
        nl = left.sum(); nr = len(y) - nl
        if nl == 0 or nr == 0:
            return None
        yl, yr = y[left], y[~left]
        sl = self.calc_std(yl)
        sr = self.calc_std(yr)
        Q = self.std - (nl/len(y))*sl - (nr/len(y))*sr
        return {"Q": Q, "threshold": thr, "left_mask": left, "lstd": sl, "rstd": sr}

    def find_optimal_split(self):
        if self.stop:
            self.best_threshold = None
            return None

        best = None
        best_column = None

        if self.ERT:
            columns_to_check = np.random.choice(self.X.shape[1], int(np.sqrt(self.X.shape[1])), replace=False)
        else:
            columns_to_check = range(self.X.shape[1])

        for column in columns_to_check:
            if self.ERT:
                result = self._ERT_split_for_column(self.X[:, column], self.y)
            else:
                result = self._best_split_for_column(self.X[:, column], self.y)

            if result is None:
                continue
            if best is None or result["Q"] > best["Q"]:
                best = result
                best_column = column

        if best is None:
            self.best_threshold = None
            return None

        left_mask = best["left_mask"]
        right_mask = ~left_mask

        self.best_Q = best["Q"]
        self.best_threshold = {
            "column": best_column,
            "row": best["threshold"],
            "left_mask": left_mask,
            "right_mask": right_mask,
            "lstd": best["lstd"],
            "rstd": best["rstd"],
        }
        return self.best_threshold

    def step(self):
        self.find_optimal_split()

        if self.best_threshold is None:
            self.stop = True
            return None

        left_mask = self.best_threshold["left_mask"]
        right_mask = self.best_threshold["right_mask"]

        childl_stop = self.best_threshold["lstd"] == 0
        childr_stop = self.best_threshold["rstd"] == 0

        self.childl = MyNodeRegressor(
            self.X[left_mask],
            self.y[left_mask],
            stop=childl_stop,
            curr_depth=self.curr_depth + 1,
            max_depth=self.max_depth,
            ERT=self.ERT,
            verbose=self.verbose,
            rng=self.rng
        )
        self.childr = MyNodeRegressor(
            self.X[right_mask],
            self.y[right_mask],
            stop=childr_stop,
            curr_depth=self.curr_depth + 1,
            max_depth=self.max_depth,
            ERT=self.ERT,
            verbose=self.verbose,
            rng=self.rng
        )
        return self.best_threshold
