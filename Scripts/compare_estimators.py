from pandas import DataFrame, concat, read_csv
from Modules.params import get_params
from Modules.functions import ls
from os.path import join
from sys import argv


def get_header(file: str) -> str:
    header = file.split("_")
    header = " ".join(header[:2])
    return header


def get_reports(models: str,
                params: dict) -> DataFrame:
    reports = DataFrame()
    if models == "classical":
        models_list = params["classical models"]
        models_path = params["Classical model path"]
    if models == "neural":
        models_list = params["neural models"]
        models_path = params["Neural model path"]
    for model in models_list:
        model = model.replace(" ",
                              "_")
        folder = join(params["path results"],
                      models_path,
                      model)
        files = ls(folder)
        files = [file
                 for file in files
                 if ".csv" in file]
        model_report = DataFrame()
        for file in files:
            filename = join(folder,
                            file)
            report = read_csv(filename,
                              index_col=0)
            value = report[params["station"]]["accuracy"]
            header = get_header(file)
            value = DataFrame(value,
                              columns=[header],
                              index=[model])
            model_report = concat([
                model_report,
                value
            ],
                axis=1)
        reports = concat([
            reports,
            model_report
        ])
    return reports


params = get_params()
params.update({
    "station": argv[1],
})
reports_classical = get_reports("classical",
                                params)
reports_neural = get_reports("neural",
                             params)
reports = concat([reports_classical,
                 reports_neural])
reports.index = [index.replace("_", " ")
                 for index in reports.index]
print(reports)
