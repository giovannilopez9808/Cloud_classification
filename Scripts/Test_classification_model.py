"""
python classification_model.py (classification_model) (station)
"""
from Modules.classic_models import classification_model
from Modules.dataset_model import dataset_model
from Modules.functions import (get_confusion_matrix,
                               get_labels,
                               get_report,
                               mkdir)
from Modules.params import get_params
from os.path import join
from tqdm import tqdm
from sys import argv


params = get_params()
params.update({
    # Define classical model
    "classification model": argv[1],
    "station": argv[2],
    "hour initial": 7,
    "hour final": 20,
})
model_name = params["classification model"]
model_name = model_name.replace(" ",
                                "_")
folder = join(params["path results"],
              params["Classical model path"],
              model_name,
              params["station"])
mkdir(folder)
# Select classical model
model = classification_model()
model.define_model(params)
# Initialize results
reports = ""
bar = tqdm(params["clear sky models"])
for sky_model in bar:
    # Select clear sky model
    params["clear sky model"] = sky_model
    for operation in params["comparison operations"]:
        # Select comparison operation
        params["comparison operation"] = operation
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
        filename = "{}_{}_matrix.csv".format(operation,
                                             sky_model)
        filename = join(folder,
                        filename)
        matrix.to_csv(filename)
filename = "report.csv"
filename = join(folder,
                filename)
file = open(filename, "w")
file.write(reports)
file.close()
