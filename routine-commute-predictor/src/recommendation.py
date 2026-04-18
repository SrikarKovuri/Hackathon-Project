from __future__ import annotations

from typing import Dict, List


def choose_best_route(route_options: List[Dict]) -> Dict:
    if not route_options:
        return {}

    return min(route_options, key=lambda x: x.get("stress", 100))


def classify_route_status(route: Dict, best_route_name: str) -> str:
    if route.get("name") == best_route_name:
        return "Recommended"

    stress = route.get("stress", 100)
    reliability = route.get("reliability", 0)

    if stress >= 70 or reliability < 60:
        return "At risk"
    if stress <= 45 and reliability >= 70:
        return "Stable"

    return "Alternative"


def attach_route_statuses(route_options: List[Dict]) -> List[Dict]:
    if not route_options:
        return []

    best_route = choose_best_route(route_options)
    best_name = best_route.get("name", "")

    updated = []
    for route in route_options:
        route_copy = route.copy()
        route_copy["status"] = classify_route_status(route_copy, best_name)
        updated.append(route_copy)

    return updated


def generate_recommendation_message(route_options: List[Dict]) -> str:
    if not route_options:
        return "No recommendation available."

    best_route = choose_best_route(route_options)
    usual_route = next((r for r in route_options if r.get("name") == "Usual route"), None)

    if not usual_route:
        return f"Best option today: {best_route.get('name', 'Unknown route')}."

    if best_route.get("name") == usual_route.get("name"):
        return "Your usual route remains the best choice today."

    stress_diff = usual_route.get("stress", 0) - best_route.get("stress", 0)
    time_diff = best_route.get("duration", 0) - usual_route.get("duration", 0)

    return (
        f"Switch to {best_route.get('name')} today. "
        f"It reduces stress by about {round(stress_diff)} points "
        f"while changing travel time by {time_diff:+} minutes."
    )