from Modules.report_reader import Report_reader
from Modules.functions import get_group_model
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "model name": argv[3],
})
params["model type"] = get_group_model(params["model name"],
                                       params)
resume = DataFrame()
for station in params["stations"]:
    params["station"] = station
    report_model = Report_reader(params)
    report = report_model.run(params["model type"])
    report.columns = [station]
    resume = concat([resume,
                     report],
                    axis=1)
folder = params["model type"].replace(" ",
                                      "_")
model = params["model name"].replace(" ",
                                     "_")
folder = join(params["path results"],
              folder,
              model)
filename = "{}_{}_resume.csv".format(params["comparison operation"],
                                     params["clear sky model"])
filename = join(folder,
                filename)
resume.to_csv(filename)
