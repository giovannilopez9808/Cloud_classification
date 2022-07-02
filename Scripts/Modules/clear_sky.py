"""
Modelo para dias de cielo despejado a partir de la ecuacion de irradiancia 
solar extraterrestre
"""
from pandas import DataFrame, to_datetime
from .GHI_model import GHI_model
from .RS_model import RS_model


class clear_sky_model:
    def __init__(self) -> None:
        """
        Creacion del modelo
        """
        pass

    def run(self, params: dict) -> DataFrame:
        """
        Realiza los calculos minuto a minuto de la irradiancia solar
        extraterrestre dada la fecha, una hora inicial, hora final y la
        posicion

        Input:
        --------------------
        Params -> diccionario con las siguientes caracteristicas
            hour initial -> hora inicial del calculo
            hour final -> hora final del calculo
            date -> dia del calculo
            longitude -> posicion en la longitud del lugar
            latitude -> posicion en la latitud del lugar
            timezone -> zona horaria del lugar

        Output:
        --------------------
        DataFrame con los valores de irradiancia minuto a minuto
        """
        # Inicializacion del modelo
        self._select_model(params)
        # Inicializacion de los resultados
        results = DataFrame(columns=["H0"])
        # Hora inicial
        hour_inital = params["hour initial"]
        # Hora incial en minutos
        hour_inital *= 60
        # Hora final
        hour_final = params["hour final"]
        # Hora final en minutos
        hour_final *= 60
        # Minutos totales del calculo
        hours = range(hour_inital,
                      hour_final+1)
        for minutes in hours:
            # Fecha con hora con formato Y-M-D H:m
            datetime = self._get_datetime(params["date"],
                                          minutes)
            params["datetime"] = datetime
            # Irradiancia solar extraterrestre
            H0 = self.model.get_H0(params)
            # Guardado de los resultados
            results.loc[datetime] = H0
        # Formateo de la fecha
        results.index = to_datetime(results.index)
        return results

    def _select_model(self,
                      params: dict) -> None:
        if params["clear sky model"] == "GHI":
            self.model = GHI_model()
            return
        if params["clear sky model"] == "RS":
            self.model = RS_model()
            return

    def _get_time(self, minutes: int) -> str:
        """
        Obtiene la hora y minutos dado los minutos consecutivos

        Inputs:
        --------------------
        minutes -> minutos consecutivos del dia

        Output:
        --------------------
        String con el tiempo en formato H:m
        """
        # Calculo de la hora
        hour = self._get_hour(minutes)
        # Calculo de los minutos
        minute = self._get_minute(minutes)
        # Formato H:m
        time = f"{hour}:{minute}"
        return time

    def _get_hour(self, minutes: int) -> str:
        """
        Obtiene la hora dado los minutos consecutivos

        Input:
        --------------------
        minutes -> minutos consecutivos del dia

        Output:
        --------------------
        String con la hora en formato de dos digitos
        """
        hour = minutes//60
        hour = fill_number(hour,
                           2)
        return hour

    def _get_minute(self, minutes: int) -> str:
        """
        Obtiene los minutos del dia dado los minutos consecutivos

        Input:
        --------------------
        minutes -> minutos consecutivos del dia

        Output:
        --------------------
        String con los minutos en formato de dos digitos
        """
        minute = minutes % 60
        minute = fill_number(minute,
                             2)
        return minute

    def _get_datetime(self,
                      date: str,
                      minutes: int) -> str:
        """
        Obtiene el formato de  Y-M-D H:m dado el dia y los minutos consecutivos

        Input:
        --------------------
        date -> fecha en string en formatom Y-M-D
        minutes -> minutos consecutivos del dia

        Output:
        --------------------
        String de la fecha con el tiempo en formato Y-M-D H:m
        """
        time = self._get_time(minutes)
        datetime = f"{date} {time}"
        return datetime


def fill_number(number: int,
                zfill: int) -> str:
    """
    Convierte un numero a string a n caracteres, los caracteres faltantes
    seran 0

    Inputs:
    --------------------
    number -> numero a convertir
    zfill -> numero de caracteres a rellenar

    Output:
    --------------------
    numero con tipo string
    """
    return str(number).zfill(zfill)


if __name__ == "__main__":
    pass
