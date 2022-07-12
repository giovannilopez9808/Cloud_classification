"""
python classification_model.py (classification_model) (station)
"""
from Modules.classification_classic_models import classification_model
from Modules.dataset_model import dataset_model
from Modules.functions import (get_confusion_matrix,
                               get_labels,
                               get_report,
                               mkdir)
from Modules.params import get_params
from os.path import join
from sys import argv


params = get_params()
params.update({
    # Define classical model
    "classification model": argv[1],
    "station":argv[2],
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
                            operation,
                            labels)
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
