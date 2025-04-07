import math

from sunlit_terraces.services.osm_data import get_surrounding_buildings
from sunlit_terraces.services.solar_position import get_solar_position


def angle_diff(a1, a2):
    diff = abs(a1 - a2) % 360
    return diff if diff <= 180 else 360 - diff


def is_sunlit(terrace_azimuth, lat, lon, dt):
    solar = get_solar_position(lat, lon, dt)
    sun_azimuth = solar["azimuth"]
    sun_elevation = solar["altitude"]

    if sun_elevation < 5:
        return False

    diff = angle_diff(terrace_azimuth, sun_azimuth)
    return diff <= 45


def is_sunlit_with_shadow(terrace_azimuth, lat, lon, dt):
    if not is_sunlit(terrace_azimuth, lat, lon, dt):
        return False

    solar = get_solar_position(lat, lon, dt)
    sun_azimuth = solar["azimuth"]
    sun_elevation = solar["altitude"]

    # Shadow check from nearby buildings
    buildings = get_surrounding_buildings(lat, lon, radius=40)
    for b in buildings:
        dx = b["lon"] - lon
        dy = b["lat"] - lat
        distance = math.hypot(dx, dy)
        if distance == 0:
            continue
        bearing = math.degrees(math.atan2(dy, dx)) % 360
        bearing_diff = angle_diff(bearing, sun_azimuth)
        if bearing_diff < 15:
            shadow_length = b["height"] / math.tan(math.radians(sun_elevation))
            if shadow_length > distance:
                return False
    return True
