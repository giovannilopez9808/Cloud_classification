"""
Conjunto de clases para la lectura y organizacion de los archivos
"""


from pandas import (read_csv,
                    Timestamp,
                    DataFrame,
                    to_datetime,
                    to_timedelta)
from os.path import join


class SIMA_model:
    """
    Modelo que guarda la estructura de los datos de SIMA
    """

    def __init__(self) -> None:
        # Inicializacion de los datos
        self.station_data = DataFrame()

    def read(self,
             filename: str) -> DataFrame:
        """
        Lectura del archivo dado su nombre

        Input:
        --------------------
        filename -> nombre del archivo a leer


        Output:
        --------------------
        Dataframe con los datos del SIMA, el indice esta con formato de fecha
        """
        self.data = read_csv(filename,
                             header=[0, 1],
                             skiprows=[2],
                             index_col=0,
                             parse_dates=True,
                             low_memory=False)
        self.data = self.data*1000

    def get_dates(self) -> list:
        """
        Obtiene las fechas del archivo leido
        """
        dates = self.data.index.date
        dates = sorted(list(set(dates)))
        return dates

    def get_station_data(self,
                         station: str,
                         pollutant: str) -> DataFrame:
        """
        Obtiene los datos correspondientes a una estacion y a una medicion en
        particular

        Input:
        --------------------
        station -> string de la estacion a leer
        pollutant -> string del contaminante a leer

        Output:
        --------------------
        Dataframe con los datos de la estacion con el contaminante seleccionado

        """
        station = station.upper()
        self.station_data = DataFrame(self.data[(station,
                                                 pollutant)])
        self.station_data = self.station_data

    def get_data_date(self,
                      date: str) -> DataFrame:
        """
        Obtiene los datos de una fecha seleccionada, si no se han leido datos
        de una estacion en particular se tomara toda la base de datos

        Input:
        --------------------
        date -> string de la fecha en formato Y-M-D

        Output:
        --------------------
        Dataframe de los datos en la fecha seleccionada
        """
        # Mismo formato que el indice
        date = to_datetime(date)
        # Si no hay una estacion seleccionada
        if len(self.station_data) != 0:
            select_data = self.station_data.index.date == date.date()
            data = self.station_data[select_data]
            return data
        # Lee los datos generales
        select_data = self.data.index.date == date.date()
        data = self.data[select_data]
        return data

    def get_station_info(self,
                         params: dict,
                         station: str) -> dict:
        """
        Obtiene la informacion de las estaciones

        Input
        --------------------
        params -> diccionario que contiene las siguientes caracteristicas
            path data -> direccion de los datos
            stations info -> nombre del archivo con los datos de las estaciones

        Output
        --------------------
        Dataframe con los datos de las estaciones, el indice son las
        caracteristicas de la informacion y el header el nombre de las
        estaciones
        """
        # Nombre con la ruta del archivo
        filename = join(params["path data"],
                        params["stations info"])
        # Lectura
        data = read_csv(filename,
                        index_col=2)
        # Formato de la fecha
        data["Since"] = to_datetime(data["Since"],
                                    format="%d/%m/%Y")
        data = data.T
        return data[station]


class clear_sky_data:
    def __init__(self,
                 params: dict) -> None:
        """
        Clase para leer los datos producidos por el modelo de irradiancia
        solar extraterrestre

        Input:
        --------------------
        params -> diccionario con las siguientes caracteristicas
            path results -> direccion de los resultados generales
            clear sky file -> nombre del archivo que contiene los datos
        """
        self.station_data = DataFrame()
        self.params = params
        self._read()

    def _read(self) -> DataFrame:
        """
        Lectura de los archivos
        """
        # Nombre con la ruta del archivo
        filename = join(self.params["path results"],
                        self.params["clear sky file"])
        # Lectura del archivo
        self.data = read_csv(filename,
                             index_col=0,
                             parse_dates=True)

    def get_dates(self) -> list:
        """
        Obtiene las fechas del archivo leido
        """
        dates = sorted(list(set(self.data.index.date)))
        return dates

    def get_station_data(self,
                         station: str) -> DataFrame:
        """
        Obtiene la informacion de una estacion
        """
        self.station_data = DataFrame(self.data[station])

    def get_date_date(self,
                      date: str) -> DataFrame:
        """
        Obtiene los datos de una fecha seleccionada, si no se han leido datos
        de una estacion en particular se tomara toda la base de datos

        Input:
        --------------------
        date -> string de la fecha en formato Y-M-D

        Output:
        --------------------
        Dataframe de los datos en la fecha seleccionada
        """
        date = to_datetime(date)
        if len(self.station_data) != 0:
            select_data = self.station_data.index.date == date.date()
            data = self.station_data[select_data]
            return data
        select_data = self.data.index.date == date.date()
        data = self.data[select_data]
        return data


class classification_data:
    def __init__(self,
                 params: dict) -> None:
        """
        Clase para leer los datos producidos por el modelo de irradiancia
        solar extraterrestre

        Input:
        --------------------
        params -> diccionario con las siguientes caracteristicas
            path results -> direccion de los resultados generales
            classification file -> nombre del archivo que contiene los datos
        """
        self.station_data = DataFrame()
        self.params = params
        self._read()

    def _read(self) -> DataFrame:
        """
        Lectura del archivo dado su nombre

        Output:
        --------------------
        Dataframe con los datos del SIMA, el indice esta con formato de fecha
        """
        filename = join(self.params["path results"],
                        self.params["classification file"])
        self.data = read_csv(filename,
                             index_col=0,
                             parse_dates=True)
        # self.data = self.data.fillna(-1)

    def get_dates(self) -> list:
        """
        Obtiene las fechas del archivo leido
        """
        dates = sorted(list(set(self.data.index.date)))
        return dates

    def get_station_data(self,
                         station: str) -> DataFrame:
        """
        Obtiene la informacion de una estacion
        """
        self.station_data = DataFrame(self.data[station])

    def get_date_date(self,
                      date: str) -> DataFrame:
        """
        Obtiene los datos de una fecha seleccionada, si no se han leido datos
        de una estacion en particular se tomara toda la base de datos

        Input:
        --------------------
        date -> string de la fecha en formato Y-M-D

        Output:
        --------------------
        Dataframe de los datos en la fecha seleccionada
        """
        date = to_datetime(date)
        if len(self.station_data) != 0:
            data = self.station_data.loc[date]
            return data
        data = self.data.loc[date]
        return data

    def get_data_from_type(self,
                           data_type: int) -> DataFrame:
        if len(self.station_data) != 0:
            data = self.station_data[self.station_data == data_type]
            data = data.dropna()
            return data


class comparison_data:
    def __init__(self,
                 params: dict) -> None:
        self.params = params

    def read(self, file: str) -> DataFrame:
        filename = f"{file}.csv"
        filename = join(self.params["path results"],
                        filename)
        self.data = read_csv(filename,
                             index_col=0,
                             parse_dates=True)

    def get_daily_mean(self) -> DataFrame:
        daily = self.data.resample("D").median()
        return daily

    def get_data_per_dates(self,
                           dates: list) -> DataFrame:
        data = self.data.loc[dates]
        return data


if __name__ == "__main__":
    pass
