"""
Proximity Service
-----------------
Finds the nearest stores to a user using the Haversine formula.
No external dependencies beyond the standard library.

Run standalone: python proximity_service.py
"""

import math
from typing import TypedDict


class Store(TypedDict):
    name: str
    lat: float
    lon: float


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute the great-circle distance between two GPS points (in kilometres).

    Uses the Haversine formula:
        a = sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2)
        c = 2·atan2(√a, √(1−a))
        d = R·c
    """
    R = 6371.0  # Earth's mean radius in km

    # Convert degrees → radians
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)

    a = math.sin(Δφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 4)


def find_nearest_store(
    user_location: tuple[float, float],
    stores: list[Store],
) -> list[dict]:
    """
    Sort stores by distance from the user's GPS location.

    Args:
        user_location: (latitude, longitude) of the user.
        stores:        List of store dicts with keys 'name', 'lat', 'lon'.

    Returns:
        Stores sorted nearest-first, each augmented with a 'distance_km' key.
    """
    user_lat, user_lon = user_location

    ranked = []
    for store in stores:
        dist = haversine_km(user_lat, user_lon, store["lat"], store["lon"])
        ranked.append({**store, "distance_km": dist})

    ranked.sort(key=lambda s: s["distance_km"])
    return ranked


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    user_location = (13.0827, 80.2707)  # Chennai, India

    stores: list[Store] = [
        {"name": "FreshMart",   "lat": 13.08, "lon": 80.27},
        {"name": "CityGrocer",  "lat": 13.10, "lon": 80.25},
        {"name": "QuickBasket", "lat": 13.07, "lon": 80.28},
    ]

    print(f"User location: {user_location}\n")
    results = find_nearest_store(user_location, stores)

    print("Stores sorted by distance:")
    for rank, store in enumerate(results, 1):
        print(f"  {rank}. {store['name']}  — {store['distance_km']} km")
