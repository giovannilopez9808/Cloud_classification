from pandas import to_timedelta, date_range
from Modules.data_model import data_model
from pvlib.location import Location
import matplotlib.pyplot as plt
from os.path import join

params = {
    "path data": "../../Data/Monterrey",
    "Date": "2020-11-01'",
    "station": "NORESTE",
    "pollutant": "SR",
}
filename = join(params["path data"],
                "2020.csv")
data = data_model()
# Lectura de los datos
data.read(filename)
# Selecciona unicamente una columna de datos
data.get_station_data(params["station"],
                      params["pollutant"])
# Selecciona el dia que se quiere obtener
data = data.get_data_date(params["Date"])
# Inicializacion de la posicion
location = Location(
    25.670,
    -100.338,
    'America/Monterrey',
    560,
    'Centro',
)

times = date_range(
    params["Date"],
    periods=60 * 24,
    freq='1min',
    tz=location.tz,
)
print(times)
model = location.get_clearsky(
    times,
    linke_turbidity=5,
)

results = model.groupby(model.index.hour).mean()
plt.plot(
    data.index+to_timedelta("00:45:00"),
    results["ghi"],
    label="GHI",
)
plt.plot(
    data*1000,
    ls="--",
    marker=".",
    label="Measurement",
)
plt.legend()
plt.show()
