import datetime

from pysolar.solar import get_altitude, get_azimuth


def get_solar_position(lat, lon, time=None):
    if time is None:
        time = datetime.datetime.utcnow()
    elevation = get_altitude(lat, lon, time)
    azimuth = get_azimuth(lat, lon, time)
    return {"altitude": elevation, "azimuth": azimuth}
