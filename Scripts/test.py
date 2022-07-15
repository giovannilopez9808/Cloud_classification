from Modules.report_reader import Report_reader
from Modules.params import get_params
from sys import argv

params = get_params()
if len(argv) == 3:
    params.update({
        "model type": "Neural model",
        "comparison operation": argv[1],
        "clear sky model": argv[2],
        "model name": argv[3],
        "station": "Noroeste"
    })
if len(argv) == 2:
    params.update({
        "model type": "Classical model",
        "station": "Noroeste",
        "model name": argv[1],
    })
report_model = Report_reader(params)
report = report_model.run(params["model type"])
print(report)
