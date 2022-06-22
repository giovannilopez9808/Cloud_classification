from Modules.params import get_params
from Modules.functions import ls
from pandas import DataFrame
from os.path import join

params = get_params()
params.update({
    "station": "Noroeste",
    "template file": "Classification.csv",
})
path = join(params["path graphics"],
            "Daily")
files = ls(path)
dates = [file.split(".")[0]
         for file in files]
template = DataFrame(dates,
                     columns=["Date"])
filename = join(params["path SMARTS data"],
                params["station"],
                params["template file"])
template.to_csv(filename,
                index=False)
