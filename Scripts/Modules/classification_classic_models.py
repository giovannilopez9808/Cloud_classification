from sklearn.svm import SVC


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


if __name__ == "__main__":
    pass
