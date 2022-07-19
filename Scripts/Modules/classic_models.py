from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from .params import get_classification_params
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from numpy import round


class classification_model:
    def __init__(self) -> None:
        pass

    def define_model(self,
                     params: dict) -> None:
        self.params = get_classification_params(params)
        model_name = params["classification model"]
        if model_name == "SVM":
            self.model = SVM_model()
            return
        if model_name == "KNN":
            self.model = KNN_model()
            return
        if model_name == "Random forest":
            self.model = Random_forest_model()
            return
        if model_name == "Gaussian naive":
            self.model = Gaussian_naive_model()
            return
        if model_name == "Decision tree":
            self.model = Decision_tree_model()
            return

    def run(self,
            data: list) -> None:
        self.model.run(data,
                       self.params)

    def predict(self,
                data: list) -> None:
        results = self.model.predict(data)
        return results


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


class Random_forest_model:
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
