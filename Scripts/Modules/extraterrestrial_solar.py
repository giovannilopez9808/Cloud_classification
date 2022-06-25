from numpy import sin, cos, pi
from datetime import datetime


class extraterrestial_solar_model:
    def __init__(self) -> None:
        # Solar constant (W/m2)
        self.Isc = 1367

    def get_H0(self,
               params: dict) -> float:
        """

        """
        datetime = params["datetime"]
        phi = params["latitude"]
        lamb = params["longitude"]
        timezone = params["timezone"]
        day, hour = self._get_day_and_hour(datetime)
        delta = self._get_declination_angle(day,
                                            hour)
        omega = self._get_solar_hour_angle(day,
                                           hour,
                                           lamb,
                                           timezone)
        g0 = cos(phi)*cos(delta)*cos(omega)
        g0 += sin(phi)*sin(delta)
        g0 *= (1+0.033*cos(360*day/365))
        g0 *= self.Isc
        if g0 < 0:
            g0 = 0
        return g0

    def _get_declination_angle(self,
                               day: int,
                               hour: float) -> float:
        """

        """
        gamma = self._get_gamma(day,
                                hour)
        delta = 24.45*sin(gamma)
        delta = pi*delta/180
        return delta

    def _get_gamma(self,
                   day: int,
                   hour: float) -> float:
        gamma = 2*pi*(284+day-1+(hour-12)/24)/365
        return gamma

    def _get_eccentricity_correction(self,
                                     day: int,
                                     hour: float) -> float:
        """

        """
        gamma = self._get_gamma(day,
                                hour)
        e0 = 0.000075
        e0 += 0.001868*cos(gamma)
        e0 -= 0.032077*sin(gamma)
        e0 -= 0.014615*cos(2*gamma)
        e0 -= 0.040849*sin(2*gamma)
        e0 *= 229.18
        return e0

    def _get_solar_hour_angle(self,
                              day: int,
                              hour: float,
                              longitude: float,
                              timezone: int) -> float:
        """

        """
        hour_c = self._get_hour_correction(day,
                                           hour,
                                           longitude,
                                           timezone)
        sha = 15*(hour_c-12)
        sha = pi*sha/180
        return sha

    def _get_offset(self,
                    day: int,
                    hour: float,
                    longitude: float,
                    timezone: int) -> float:
        """

        """
        e0 = self._get_eccentricity_correction(day,
                                               hour)
        offset = e0+4*(longitude-15*timezone)
        return offset

    def _get_hour_correction(self,
                             day: int,
                             hour: float,
                             longitude: float,
                             timezone: int) -> float:
        """

        """
        offset = self._get_offset(day,
                                  hour,
                                  longitude,
                                  timezone)
        hour_corrected = hour + offset/60
        return hour_corrected

    def _get_day_and_hour(self,
                          date: str) -> tuple:
        """

        """
        date = datetime.strptime(date,
                                 "%Y-%m-%d %H:%M")
        first_date = date.replace(month=1,
                                  day=1,
                                  hour=1,
                                  minute=1)
        day = (date-first_date).days
        if day > 365:
            day = 365
        hour = self._get_hour_from_datetime(date)
        return day, hour

    def _get_hour_from_datetime(self,
                                date: datetime) -> float:
        """

        """
        hour = date.hour
        minute = date.minute
        hour += minute/60
        return hour


if "__main__" == __name__:
    pass
