"""
Obtiene uns descripcion de los valores de diferencias o razones de la medicion
con respecto al modelo escogido.
"""

from Modules.data_model import (full_comparison_data,
                                classification_data)
from Modules.functions import get_labels
from Modules.params import get_params
from pandas import DataFrame, concat
from os.path import join
# Obtiene las rutas de los archivos
params = get_params()
# Añadimos datos especiales para el programa
params.update({
    # Nombre principal del archivo de resultados
    "file results": "Full_central_tendency",
    # Operacion que comparara
    "comparison operation": "diff",
    # Modelo a comparar
    "clear sky model": "GHI",
})
# Nombres e identificadores de las clasificaciones
cloud_types, names = get_labels(params)
# Datos de las clasificacion
classification = classification_data(params)
# Datos de los vectores de comparacion
comparison = full_comparison_data(params)
# Promedio diario
daily = comparison.get_daily_mean()
# Inicializacion de los datos por clasificacion
data = dict()
for cloud_type in cloud_types:
    data[cloud_type] = []
    for station in daily.columns:
        # Obtiene la informacion de cada estacion
        classification.get_station_data(station)
        # Obtiene los valores de cada clasificacion
        values = classification.get_data_from_type(cloud_type)
        # Obtiene las fechas
        dates = values.index
        # Obtiene los valores de las fechas seleccionadas
        values = daily[station][dates]
        # Guardado de los datos
        data[cloud_type] += list(values)
    # Formato de los datos
    data[cloud_type] = DataFrame(data[cloud_type])
# Inicializacion de los resultados
results = DataFrame()
for cloud_type, name in zip(cloud_types, names):
    # Obtiene las medidas de tendencia central
    tendency = data[cloud_type].describe()
    tendency.columns = [name]
    # Guardado de los resultados
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
# Guardado de los resultados
results.to_csv(filename)
