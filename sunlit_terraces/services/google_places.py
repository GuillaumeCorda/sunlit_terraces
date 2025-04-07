import requests

from sunlit_terraces.config import GOOGLE_PLACES_API_KEY


def get_nearby_venues(location, radius, min_rating):
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={location}&radius={radius}&type=cafe"
        f"&key={GOOGLE_PLACES_API_KEY}"
    )
    response = requests.get(url)
    return response.json()
