import math

import requests


def get_terrace_orientation(lat, lon):
    """
    Query Overpass API for nearby building ways with outdoor seating or terraces
    and calculate orientation based on wall segment closest to the location.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      way(around:30,{lat},{lon})["outdoor_seating"];
      way(around:30,{lat},{lon})["terrace"];
      way(around:30,{lat},{lon})["building"];
    );
    (._;>;);
    out body;
    """

    try:
        response = requests.post(overpass_url, data={"data": query})
        data = response.json()

        # Index all nodes by ID
        node_map = {el["id"]: el for el in data["elements"] if el["type"] == "node"}
        ways = [el for el in data["elements"] if el["type"] == "way"]

        def compute_orientation(node1, node2):
            dx = node2["lon"] - node1["lon"]
            dy = node2["lat"] - node1["lat"]
            angle = math.degrees(math.atan2(dy, dx))
            return (angle + 360) % 360

        best_orientation = None
        min_distance = float("inf")

        for way in ways:
            nodes = [
                node_map.get(nid) for nid in way.get("nodes", []) if node_map.get(nid)
            ]
            for i in range(len(nodes) - 1):
                n1, n2 = nodes[i], nodes[i + 1]
                mid_lat = (n1["lat"] + n2["lat"]) / 2
                mid_lon = (n1["lon"] + n2["lon"]) / 2
                dist = math.hypot(mid_lat - lat, mid_lon - lon)
                if dist < min_distance:
                    min_distance = dist
                    best_orientation = compute_orientation(n1, n2)

        if best_orientation is not None:
            return round(best_orientation, 2)
        return None

    except Exception as e:
        print(f"[ERROR] Failed to fetch terrace orientation: {e}")
        return None


def get_surrounding_buildings(lat, lon, radius=40):
    import requests

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      way(around:{radius},{lat},{lon})["building"]["height"];
      way(around:{radius},{lat},{lon})["building:levels"];
    );
    (._;>;);
    out body;
    """
    try:
        res = requests.post(overpass_url, data={"data": query})
        data = res.json().get("elements", [])
        ways = [el for el in data if el["type"] == "way"]
        results = []

        for way in ways:
            tags = way.get("tags", {})
            h = tags.get("height")
            if not h and "building:levels" in tags:
                h = str(float(tags["building:levels"]) * 3.0)
            if h:
                results.append(
                    {
                        "height": float(h),
                        "lat": way["center"]["lat"] if "center" in way else lat,
                        "lon": way["center"]["lon"] if "center" in way else lon,
                    }
                )
        return results
    except Exception as e:
        print(f"[ERROR] Cannot fetch building heights: {e}")
        return []
