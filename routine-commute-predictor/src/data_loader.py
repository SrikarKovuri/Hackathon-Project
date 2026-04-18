from pathlib import Path
import json
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _safe_read_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _safe_read_json(filename: str) -> Any:
    path = DATA_DIR / filename
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_stations() -> pd.DataFrame:
    return _safe_read_csv("stations.csv")


def load_routes() -> pd.DataFrame:
    return _safe_read_csv("routes.csv")


def load_trips() -> pd.DataFrame:
    return _safe_read_csv("trips.csv")


def load_delays() -> pd.DataFrame:
    return _safe_read_csv("delays.csv")


def load_disruptions() -> pd.DataFrame:
    return _safe_read_csv("disruptions.csv")


def load_commute_history() -> pd.DataFrame:
    return _safe_read_csv("mock_commute_history.csv")


def load_user_profiles() -> dict:
    data = _safe_read_json("sample_user_profiles.json")
    return data if isinstance(data, dict) else {}


def load_bike_lockers_sheds() -> pd.DataFrame:
    return _safe_read_csv("bike_lockers_sheds.csv")


def load_bus_shelters_geojson() -> dict:
    data = _safe_read_json("Bus_shelters.geojson")
    return data if isinstance(data, dict) else {}


def load_bus_shelters_as_dataframe() -> pd.DataFrame:
    geojson = load_bus_shelters_geojson()
    features = geojson.get("features", [])

    rows = []
    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        coords = geometry.get("coordinates", [])

        if geometry.get("type") == "Point" and len(coords) >= 2:
            rows.append(
                {
                    "Longitude": coords[0],
                    "Latitude": coords[1],
                    **properties,
                }
            )

    return pd.DataFrame(rows)