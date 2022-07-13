from Modules.params import get_params
from Modules.functions import ls
from pandas import DataFrame
from os.path import join

params = get_params()
path = join(params["path graphics"],
            "RS",
            "Daily",
            params["stations"][0])
files = ls(path)
dates = [file.split(".")[0]
         for file in files]
template = DataFrame(index=dates,
                     columns=params["stations"])
filename = join(params["path results"],
                params["classification file"])
template.index.name = "Date"
template.to_csv(filename)
