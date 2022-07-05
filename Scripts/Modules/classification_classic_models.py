from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from numpy import round


class SVM_model:
    def __init__(self) -> None:
        pass

    def run(self,
            data: list,
            params: dict) -> None:
        vectors, target = data
        self.model = SVC(**params)
        self.model.fit(vectors,
                       target)

    def predict(self,
                data: list) -> list:
        vectors, _ = data
        results = self.model.predict(vectors)
        return results


class KNN_model:
    def __init__(self) -> None:
        pass

    def run(self,
            data: list,
            params: dict) -> None:
        self.model = KNeighborsRegressor(**params)
        vectors, target = data
        self.model.fit(vectors,
                       target)

    def predict(self,
                data: list) -> list:
        vectors, _ = data
        results = self.model.predict(vectors)
        results = round(results)
        return results


class random_forest_model:
    def __init__(self) -> None:
        pass

    def run(self,
            data: list,
            params: dict) -> None:
        vectors, target = data
        self.model = RandomForestClassifier(**params)
        self.model.fit(vectors,
                       target)

    def predict(self,
                data: list) -> list:
        vectors, _ = data
        results = self.model.predict(vectors)
        return results


class Gaussian_naive_model:
    def __init__(self) -> None:
        pass

    def run(self,
            data: list,
            params: dict) -> None:
        vectors, target = data
        self.model = GaussianNB(**params)
        self.model.fit(vectors,
                       target)

    def predict(self,
                data: list) -> list:
        vectors, _ = data
        results = self.model.predict(vectors)
        return results


class Decision_tree_model:
    def __init__(self) -> None:
        pass

    def run(self,
            data: list,
            params: dict) -> None:
        vectors, target = data
        self.model = DecisionTreeClassifier(**params)
        self.model.fit(vectors,
                       target)

    def predict(self,
                data: list) -> list:
        vectors, _ = data
        results = self.model.predict(vectors)
        return results


if __name__ == "__main__":
    pass
