from Modules.functions import fill_number, yyyy_mm_dd2yymmdd
from pandas import read_csv, Timestamp, DataFrame
from os.path import join

params = {
    "path data": "../Data",
    "path results": "SMARTS/Data/Centro",
    "path OMI": "OMI",
    "AOD file": "AOD.csv",
    "Ozone file": "Ozone.csv",
}

filename = join(params["path data"],
                params["path OMI"],
                params["Ozone file"])
Ozone = read_csv(filename,
                 index_col=0,
                 parse_dates=True)
filename = join(params["path data"],
                params["path OMI"],
                params["AOD file"])
AOD = read_csv(filename,
               index_col=0,
               parse_dates=True)
data = DataFrame(columns=["Date",
                          "ozone",
                          "AOD",
                          "year",
                          "month",
                          "day"])
for i, date in enumerate(AOD.index):
    aod = AOD["500nm"][date]
    ozone = Ozone["Ozone"][date]
    day = date.day
    month = date.month
    year = date.year
    date = yyyy_mm_dd2yymmdd(date)
    data.loc[i] = [date,
                   ozone,
                   aod,
                   year, month,
                   day]
filename = join(params["path results"],
                "datos.txt")
data.to_csv(filename,
            index=False)
