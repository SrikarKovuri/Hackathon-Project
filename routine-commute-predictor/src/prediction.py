from __future__ import annotations

from typing import Dict, List

import pandas as pd

from src.stress_score import (
    calculate_base_stress_score,
    personalise_stress_score,
    interpret_stress_level,
)


def get_demo_route_options(profile: Dict) -> List[Dict]:
    """
    Returns demo route options for hackathon use.
    This can later be replaced with real route generation from NSW data.
    """
    origin = profile.get("origin", "Parramatta")
    destination = profile.get("destination", "Central")

    return [
        {
            "name": "Usual route",
            "origin": origin,
            "destination": destination,
            "duration": 41,
            "transfers": 2,
            "delay_risk": 0.62,
            "crowding_level": 0.70,
            "walking_minutes": 6,
            "reliability": 61,
            "notes": "Fastest on paper, but sensitive to delays.",
        },
        {
            "name": "Lower-stress option",
            "origin": origin,
            "destination": destination,
            "duration": 46,
            "transfers": 0,
            "delay_risk": 0.20,
            "crowding_level": 0.35,
            "walking_minutes": 3,
            "reliability": 86,
            "notes": "Direct service with better reliability this morning.",
        },
        {
            "name": "Balanced option",
            "origin": origin,
            "destination": destination,
            "duration": 43,
            "transfers": 1,
            "delay_risk": 0.35,
            "crowding_level": 0.50,
            "walking_minutes": 4,
            "reliability": 73,
            "notes": "Slightly longer but safer than your usual route.",
        },
    ]


def score_route_options(profile: Dict, route_options: List[Dict]) -> List[Dict]:
    walking_tolerance = int(profile.get("walking_tolerance", 8))
    weights = profile.get("weights", {"speed": 30, "stress": 50, "reliability": 20})

    scored = []
    for route in route_options:
        base_stress = calculate_base_stress_score(
            duration_min=route["duration"],
            transfers=route["transfers"],
            delay_risk=route["delay_risk"],
            crowding_level=route["crowding_level"],
            walking_minutes=route["walking_minutes"],
            reliability_score=route["reliability"],
            walking_tolerance=walking_tolerance,
        )

        personalised_score = personalise_stress_score(
            base_stress=base_stress,
            weights=weights,
            duration_min=route["duration"],
            reliability_score=route["reliability"],
        )

        route_copy = route.copy()
        route_copy["base_stress"] = base_stress
        route_copy["stress"] = personalised_score
        route_copy["stress_label"] = interpret_stress_level(personalised_score)
        scored.append(route_copy)

    return scored


def build_today_summary(profile: Dict, scored_routes: List[Dict]) -> Dict:
    usual_route = next((r for r in scored_routes if r["name"] == "Usual route"), scored_routes[0])
    best_route = min(scored_routes, key=lambda x: x["stress"])

    if best_route["name"] == usual_route["name"]:
        recommendation = f"Your usual route is still your best option this morning."
    else:
        recommendation = (
            f"Take the {best_route['name'].lower()} instead of your usual route."
        )

    alert = (
        "Tighter transfer windows and elevated delay risk are affecting parts of your normal commute."
        if usual_route["stress"] >= 50
        else "Network conditions look relatively stable this morning."
    )

    return {
        "expected_duration": usual_route["duration"],
        "stress_score": round(usual_route["stress"]),
        "reliability": reliability_band(usual_route["reliability"]),
        "alert": alert,
        "recommendation": recommendation,
        "usual_route": f"{profile.get('origin', 'Origin')} → {profile.get('destination', 'Destination')}",
        "reason_1": "Your normal route is being evaluated using reliability, transfers, and delay exposure.",
        "reason_2": "Today’s recommendation is adjusted to match your personal stress and reliability preferences.",
        "reason_3": f"{best_route['name']} currently provides the strongest balance of comfort and certainty.",
    }


def reliability_band(score: float) -> str:
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def routes_to_dataframe(scored_routes: List[Dict]) -> pd.DataFrame:
    if not scored_routes:
        return pd.DataFrame()

    df = pd.DataFrame(scored_routes)
    rename_map = {
        "name": "name",
        "duration": "duration",
        "transfers": "transfers",
        "stress": "stress",
        "reliability": "reliability",
        "notes": "notes",
    }
    return df[list(rename_map.keys())].copy()