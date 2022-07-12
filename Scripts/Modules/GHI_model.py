"""
Modelo de la irradiancia solar extraterrestre para una locacion y tiempo
definido
"""
from numpy import sin, cos, pi
from datetime import datetime


class GHI_model:
    def __init__(self) -> None:
        # Solar constant (W/m2)
        self.Isc = 1367

    def run(self,
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
        g0 = self._get_zenith_angle(phi,
                                    delta,
                                    omega)
        g0 *= (1+0.033*cos(360*day/365))
        g0 *= self.Isc
        # Si es negativo, entonces el valor es 0
        if g0 < 0:
            g0 = 0
        return g0

    def _get_zenith_angle(self,
                          phi: float,
                          delta: float,
                          omega: float) -> float:
        cos_z = cos(phi)*cos(delta)*cos(omega)
        cos_z += sin(phi)*sin(delta)
        return cos_z

    def _get_declination_angle(self,
                               day: int,
                               hour: float) -> float:
        """
        Obtiene el angulo de declinacion solar

        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal

        Output:
        --------------------
        Angulo de declinacion en la fecha y hora
        """
        gamma = self._get_gamma(day,
                                hour)
        delta = 24.45*sin(gamma)
        delta = self._to_radian(delta)
        return delta

    def _get_gamma(self,
                   day: int,
                   hour: float) -> float:
        """
        Obtiene la fraccion de la rotacion de la tierra
        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal

        Output:
        --------------------
        Angulo
        """
        # gamma = 284+day+hour/24
        gamma = day-81
        gamma = 2*pi*gamma/365
        return gamma

    def _get_eccentricity_correction(self,
                                     day: int,
                                     hour: float) -> float:
        """
        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal

        Output:
        --------------------
        valor de la eccentricidad
        """
        gamma = self._get_gamma(day,
                                hour)
        e0 = 9.87*sin(2*gamma)
        e0 -= 7.53*cos(gamma)
        e0 -= 1.5*sin(gamma)
        return e0

    def _get_solar_hour_angle(self,
                              day: int,
                              hour: float,
                              longitude: float,
                              timezone: int) -> float:
        """
        Obtiene el angulo solar dado la hora, fecha, longitud y zona
        horaria del lugar

        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal
        longitude -> longitud del lugar
        timezone -> zona horaria

        Output:
        --------------------
        valor del angulo horario solar
        """
        hour_c = self._get_local_solar_time(day,
                                            hour,
                                            longitude,
                                            timezone)
        sha = 15*(hour_c-12)
        sha = self._to_radian(sha)
        return sha

    def _get_time_correction_factor(self,
                                    day: int,
                                    hour: float,
                                    longitude: float,
                                    timezone: int) -> float:
        """
        Correccion horaria

        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal
        longitude -> longitud del lugar
        timezone -> zona horaria

        Output:
        --------------------
        correccion longitudinal
        """
        e0 = self._get_eccentricity_correction(day,
                                               hour)
        offset = e0+4*(longitude-15*timezone)
        return offset

    def _get_local_solar_time(self,
                              day: int,
                              hour: float,
                              longitude: float,
                              timezone: int) -> float:
        """
        Input:
        --------------------
        day -> dia consecutivo
        hour -> hora con los minutos en decimal
        longitude -> longitud de la locacion
        timezone -> zona horaria

        Output:
        --------------------
        correccion de la hora
        """
        tc = self._get_time_correction_factor(day,
                                              hour,
                                              longitude,
                                              timezone)
        hour_corrected = hour + tc/60
        return hour_corrected

    def _get_day_and_hour(self,
                          date: str) -> tuple:
        """
        Obtiene el dia consecutivo y la hora con minutos en decimal

        Inputs:
        --------------------
        date -> fecha con formato Y-M-D

        Output:
        --------------------
        dia consecutivo y hora con minutos en decimal
        """
        date = datetime.strptime(date,
                                 "%Y-%m-%d %H:%M")
        # Primer dia del año
        first_date = date.replace(month=1,
                                  day=1,
                                  hour=1,
                                  minute=1)
        # Numero de dias consecutivos
        day = (date-first_date).days
        if day > 365:
            day = 365
        # Hora
        hour = self._get_hour_from_datetime(date)
        return day, hour

    def _get_hour_from_datetime(self,
                                date: datetime) -> float:
        """
        Obtiene la hora con minutos en decimal

        Inputs
        --------------------
        date -> fecha con formato datetime

        Output:
        --------------------
        hora con minutos en decimal
        """
        hour = date.hour
        minute = date.minute
        hour += minute/60
        return hour

    def _to_radian(self,
                   degree: float) -> float:
        rad = pi*degree/180
        return rad

    def _to_degree(self,
                   radian: float) -> float:
        degree = 180*radian/pi
        return degree


if "__main__" == __name__:
    pass
