import os
import urllib.parse
from datetime import datetime
from datetime import time as dt_time
from datetime import timezone

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Query

from sunlit_terraces.services.osm_data import get_terrace_orientation
from sunlit_terraces.services.solar_position import get_solar_position
from sunlit_terraces.services.sunlight_filter import is_sunlit

load_dotenv()
router = APIRouter()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

TYPES = ["bar", "cafe", "restaurant", "pub"]


def parse_hour_to_datetime(hour_str):
    h, m = map(int, hour_str.strip().split(":"))
    today = datetime.now(timezone.utc).date()
    return datetime.combine(today, dt_time(hour=h, minute=m, tzinfo=timezone.utc))


@router.get("/")
def get_venues(location: str = Query(...), radius: int = 1000, hour: str = None):
    try:
        query_time = parse_hour_to_datetime(hour)
    except Exception as e:
        print(e)
        return {"error": "Invalid time format. Use HH:MM"}

    # Step 1: Geocode
    encoded_location = urllib.parse.quote(location)
    geocode_url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={encoded_location}&key={GOOGLE_API_KEY}"
    )
    geo_data = requests.get(geocode_url).json()
    if not geo_data.get("results"):
        return {
            "venues": [],
            "location": None,
            "error": "Invalid location",
        }

    loc = geo_data["results"][0]["geometry"]["location"]
    lat, lng = loc["lat"], loc["lng"]

    # Step 2: Solar info
    sun = get_solar_position(lat, lng, query_time)
    if sun["altitude"] < 5:
        return {
            "venues": [],
            "location": {"lat": lat, "lng": lng},
            "sunlit": False,
        }

    # Step 3: Google Places
    venues = []
    seen_ids = set()
    for place_type in TYPES:
        url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}&radius={radius}&type={place_type}"
            f"&key={GOOGLE_API_KEY}"
        )
        res = requests.get(url).json()
        for place in res.get("results", []):
            pid = place.get("place_id")
            name = place.get("name")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)

            plat = place["geometry"]["location"]["lat"]
            plng = place["geometry"]["location"]["lng"]
            address = place.get("vicinity")
            rating = place.get("rating")

            # Step 4: Orientation
            orientation = get_terrace_orientation(plat, plng)
            if orientation is None:
                continue  # skip if orientation unknown

            if is_sunlit(orientation, lat, lng, query_time):
                venues.append(
                    {
                        "id": pid,
                        "name": name,
                        "lat": plat,
                        "lng": plng,
                        "rating": rating,
                        "address": address,
                        "maps_url": (
                            "https://www.google.com/maps/place/"
                            f"?q=place_id:{pid}"
                        ),
                    }
                )

    return {
        "location": {"lat": lat, "lng": lng},
        "sun_azimuth": sun["azimuth"],
        "sunlit": True,
        "venues": venues,
    }
