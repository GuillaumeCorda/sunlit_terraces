EXCLUDED_TYPES = {
    "gas_station",
    "car_wash",
    "car_repair",
    "convenience_store",
    "car_dealer",
    "atm",
    "bank",
    "insurance_agency",
}

EXCLUDED_NAME_KEYWORDS = ["shell", "esso", "bp", "garage", "gas", "fuel", "petrol"]


def is_relevant_place(place):
    name = place.get("name", "").lower()
    types = place.get("types", [])
    keywords = ["terrace", "outdoor", "roof", "patio", "deck"]

    # Basic checks on name and types
    if any(k in name for k in keywords):
        return True
    if any(t in types for t in ["restaurant", "bar", "cafe"]):
        if "gas_station" not in types:
            return True

    # Optional: check user-ratings-total or presence of photos
    return False
