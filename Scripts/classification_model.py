"""
python classification_model.py (classification_model)
"""
from Modules.classification_classic_models import classification_model
from sklearn.metrics import (classification_report,
                             confusion_matrix)
from Modules.dataset_model import dataset_model
from Modules.functions import (get_labels,
                               mkdir)
from Modules.params import get_params
from pandas import DataFrame
from os.path import join
from sys import argv


def get_report(target: list,
               predict: list,
               sky_model: str,
               operation: str) -> str:
    header = "-"*60
    results = header
    results += f"\n\t\tSky model: {sky_model}\tOperation: {operation}\n"
    results += header+"\n"
    report = classification_report(target,
                                   predict,
                                   target_names=labels)
    results += report
    return results


def get_confusion_matrix(target: list,
                         predict: list,
                         labels: list) -> DataFrame:
    matrix = confusion_matrix(target,
                              predict)
    matrix = DataFrame(matrix,
                       index=labels,
                       columns=labels)
    return matrix


params = get_params()
params.update({
    # Define classical model
    "classification model": argv[1],
    "hour initial": 5,
    "hour final": 19,
})
model_name = params["classification model"]
model_name = model_name.replace(" ",
                                "_")
folder = join(params["path results"],
              params["Classical model path"],
              model_name)
mkdir(folder)
# Select classical model
model = classification_model()
model.define_model(params)
# Initialize results
# results = DataFrame
reports = ""
for sky_model in params["clear sky models"]:
    # Select clear sky model
    params["clear sky model"] = sky_model
    for operation in params["comparison operations"]:
        # Select comparison operation
        params["comparison operation"] = operation
        print("-"*40)
        print("Sky model: {}\tOperation: {}".format(sky_model,
                                                    operation))
        # Get labels per classification
        _, labels = get_labels(params)
        # Get dataset
        dataset = dataset_model(params)
        dataset.split_data()
        # Run classical model
        model.run(dataset.train)
        # Prediction
        result = model.predict(dataset.test)
        report = get_report(dataset.test[1],
                            result,
                            sky_model,
                            operation)
        reports += report
        matrix = get_confusion_matrix(dataset.test[1],
                                      result,
                                      labels)
        # filename = "{}_{}_matrix.csv".format(operation,
        # sky_model)
        # filename = join(folder,
        # filename)
        # matrix.to_csv(filename)
        print(matrix)
print(reports)
# filename = "report.csv"
# filename = join(folder,
# filename)
# file = open(filename, "w")
# file.write(reports)
# file.close()
