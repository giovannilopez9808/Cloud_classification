"""

"""
from Modules.data_model import (comparison_data,
                                classification_data)
from Modules.functions import get_labels
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join

# Rutas y nombres de archivos
params = get_params()
# Añadidos del programa
params.update({
    # Nombre del archivo de resultados
    "file results": "Central_tendency",
    # Operacion de comparacion
    "comparison operation": "diff",
    # Modelo a comparar
    "clear sky model": "RS",
})
# Identificador y nombre de las clasificaciones
cloud_types, names = get_labels(params)
# Valores de cada clasificacion
classification = classification_data(params)
# Vectores de comparacion
comparison = comparison_data(params)
# Promedios diarios
daily = comparison.get_daily_mean()
# Inicializacion de los datos
data = dict()
for cloud_type in cloud_types:
    data[cloud_type] = []
    for station in daily.columns:
        # Datos para cada estacion
        classification.get_station_data(station)
        # Valores por clasificacion
        values = classification.get_data_from_type(cloud_type)
        dates = values.index
        values = daily[station][dates]
        # Guardado de los valores
        data[cloud_type] += list(values)
    # Formato
    data[cloud_type] = DataFrame(data[cloud_type])
# Inicializacion de los resultados
results = DataFrame()
for cloud_type, name in zip(cloud_types, names):
    # Medidas de tendencia central
    tendency = data[cloud_type].describe()
    tendency.columns = [name]
    results = concat([results,
                      tendency],
                     axis=1)
results.index.name = "Central tendency"
# Nombre del archivo de resultados
filename = "{}_{}.csv".format(params["file results"],
                              params["comparison operation"])
filename = join(params["path results"],
                params["clear sky model"],
                filename)
# Guardado de resultados
results.to_csv(filename)
