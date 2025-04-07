from sunlit_terraces.services.sunlight_filter import is_sunlit


def filter_venues(places, latitude, longitude, dt):
    filtered = []
    for place in places:
        orientation = place.get("orientation")
        if orientation is not None and is_sunlit(orientation, latitude, longitude, dt):
            filtered.append(place)
    return filtered
