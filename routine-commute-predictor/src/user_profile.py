from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


DEFAULT_PROFILE = {
    "name": "Nawfal",
    "origin": "Parramatta",
    "destination": "Central",
    "departure_time": "07:42",
    "arrival_goal": "08:30",
    "walking_tolerance": 8,
    "priority": "Lower stress",
    "weights": {
        "speed": 30,
        "stress": 50,
        "reliability": 20,
    },
}


@dataclass
class UserProfile:
    name: str
    origin: str
    destination: str
    departure_time: str
    arrival_goal: str
    walking_tolerance: int
    priority: str
    weights: Dict[str, int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        merged = DEFAULT_PROFILE.copy()
        merged.update(data or {})
        merged["weights"] = {
            **DEFAULT_PROFILE["weights"],
            **(data.get("weights", {}) if data else {}),
        }
        return cls(**merged)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def get_default_profile() -> Dict[str, Any]:
    return DEFAULT_PROFILE.copy()


def normalise_weights(weights: Dict[str, int]) -> Dict[str, float]:
    speed = max(0, weights.get("speed", 0))
    stress = max(0, weights.get("stress", 0))
    reliability = max(0, weights.get("reliability", 0))

    total = speed + stress + reliability
    if total == 0:
        return {"speed": 1 / 3, "stress": 1 / 3, "reliability": 1 / 3}

    return {
        "speed": speed / total,
        "stress": stress / total,
        "reliability": reliability / total,
    }


def validate_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    validated = get_default_profile()
    validated.update(profile or {})

    if not isinstance(validated.get("walking_tolerance"), int):
        try:
            validated["walking_tolerance"] = int(validated["walking_tolerance"])
        except (TypeError, ValueError):
            validated["walking_tolerance"] = DEFAULT_PROFILE["walking_tolerance"]

    weights = validated.get("weights", {})
    validated["weights"] = {
        "speed": int(weights.get("speed", DEFAULT_PROFILE["weights"]["speed"])),
        "stress": int(weights.get("stress", DEFAULT_PROFILE["weights"]["stress"])),
        "reliability": int(weights.get("reliability", DEFAULT_PROFILE["weights"]["reliability"])),
    }

    return validated