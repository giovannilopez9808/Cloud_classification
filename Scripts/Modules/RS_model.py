"""
Modelo de la irradiancia solar extraterrestre para una locacion y tiempo
definido
"""
from numpy import sin, cos, pi, exp, arccos, power
from .GHI_model import GHI_model
from datetime import datetime


class RS_model(GHI_model):
    def __init__(self) -> None:
        pass

    def get_H0(self,
               params: dict) -> float:
        """
        Obtiene el modelo de irradiancia extraterrestre para una locacion
        y tiempo definido

        Input:
        --------------------
        params -> diccionario con las siguientes caracteristicas
            datetime -> fecha y hora con el formato Y-M-D H:m
            latitude -> latitud del lugar
            longitude -> longitud del lugar
            timezone -> zona horaria del lugar

        Output:
        --------------------
        valor de irradiancia en la hora y localizacion dada
        """
        a = 1119
        b = 1.19
        c = 1e-6
        # Fecha y hora
        datetime = params["datetime"]
        # Latitud
        phi = params["latitude"]
        phi = self._to_radian(phi)
        # Longitud
        lamb = params["longitude"]
        # Zona horaria
        timezone = params["timezone"]
        # Obtiene el dia consecutivo y hora del lugar
        day, hour = self._get_day_and_hour(datetime)
        # Solar declination
        delta = self._get_declination_angle(day,
                                            hour)
        # Solar hour angle
        omega = self._get_solar_hour_angle(day,
                                           hour,
                                           lamb,
                                           timezone)
        # Ecuacion de irradiancia solar extraterrestre
        cos_z = cos(phi)*cos(delta)*cos(omega)
        cos_z += sin(phi)*sin(delta)
        if cos_z < 0:
            g0 = 0
            return g0
        z = arccos(cos_z)
        z = 180*z/pi
        g0 = power(cos_z, b)
        g0 *= a
        g0 *= exp(-c*(90-z))
        return g0


if "__main__" == __name__:
    pass
