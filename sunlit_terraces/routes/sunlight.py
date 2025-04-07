import datetime

import pysolar.solar as solar
from fastapi import APIRouter
from geopy.geocoders import Nominatim

router = APIRouter()


def get_solar_position(lat: float, lon: float):
    time = datetime.datetime.utcnow()
    altitude = solar.get_altitude(lat, lon, time)
    azimuth = solar.get_azimuth(lat, lon, time)
    return {"altitude": altitude, "azimuth": azimuth}


@router.get("/")
def check_sunlight(location: str):
    geolocator = Nominatim(user_agent="sunlit_terraces")
    loc = geolocator.geocode(location)
    if loc:
        return get_solar_position(loc.latitude, loc.longitude)
    return {"error": "Location not found"}
