"""
python classification_model.py (classification_model)
"""
from Modules.classification_classic_models import classification_model
from sklearn.metrics import classification_report
from Modules.dataset_model import dataset_model
from Modules.functions import get_labels
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
from sys import argv


def define_index(data: DataFrame,
                 model: str,
                 operation: str) -> DataFrame:
    text = "{} {} {}"
    index = [text.format(model,
                         operation,
                         value)
             for value in data.index]
    data.index = index
    return data


params = get_params()
params.update({
    "comparison operations": ["ratio",
                              "diff"],
    "classification model": argv[1],
    "clear sky models": ["RS",
                         "GHI"],
    "hour initial": 9,
    "hour final": 18,
})
model = classification_model()
model.define_model(params)
results = DataFrame()
for sky_model in params["clear sky models"]:
    params["clear sky model"] = sky_model
    for operation in params["comparison operations"]:
        params["comparison operation"] = operation
        print("-"*40)
        print("Sky model: {}\tOperation: {}".format(sky_model,
                                                    operation))
        _, labels = get_labels(params)
        dataset = dataset_model(params)
        model.run(dataset.train)
        result = model.predict(dataset.test)
        partial_results = classification_report(dataset.test[1],
                                                result,
                                                target_names=labels,
                                                output_dict=True)
        partial_results = DataFrame(partial_results)
        partial_results = define_index(partial_results,
                                       sky_model,
                                       operation)
        last_index = partial_results.index[-1]
        partial_results = partial_results.drop(last_index)
        results = concat([results,
                          partial_results])
filename = f"{params['classification model']}_results.csv"
filename = join(params["path results"],
                filename)
results.to_csv(filename)
