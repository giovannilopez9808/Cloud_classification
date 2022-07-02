from pandas import read_csv

# parameter = "PM10"
parameter = "SR"
data = read_csv("SIMA/2021.csv",
                header=[0, 1],
                skiprows=[2],
                index_col=0,
                parse_dates=True,
                low_memory=False)
columns = data.columns
columns = [(station, value)
           for station, value in columns
           if value == parameter]
data = data[columns]
data = data[data.index.hour >= 8]
data = data[data.index.hour <= 19]
data = data.resample("D").count()
data = data >= 11
# data = data >= 21
print(data.sum()/365*100)
