from __future__ import annotations

from typing import Dict


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def duration_penalty(duration_min: float) -> float:
    return min(duration_min * 0.9, 25)


def transfer_penalty(transfers: int) -> float:
    return transfers * 14


def delay_risk_penalty(delay_risk: float) -> float:
    """
    delay_risk expected on 0-1 scale
    """
    return delay_risk * 25


def crowding_penalty(crowding_level: float) -> float:
    """
    crowding_level expected on 0-1 scale
    """
    return crowding_level * 18


def walking_penalty(walking_minutes: float, tolerance: int) -> float:
    if walking_minutes <= tolerance:
        return walking_minutes * 1.2
    excess = walking_minutes - tolerance
    return tolerance * 1.2 + excess * 2.5


def reliability_penalty(reliability_score: float) -> float:
    """
    reliability_score expected on 0-100 scale, higher is better
    """
    reliability_score = clamp(reliability_score, 0, 100)
    return (100 - reliability_score) * 0.22


def calculate_base_stress_score(
    duration_min: float,
    transfers: int,
    delay_risk: float,
    crowding_level: float,
    walking_minutes: float,
    reliability_score: float,
    walking_tolerance: int,
) -> float:
    score = (
        duration_penalty(duration_min)
        + transfer_penalty(transfers)
        + delay_risk_penalty(delay_risk)
        + crowding_penalty(crowding_level)
        + walking_penalty(walking_minutes, walking_tolerance)
        + reliability_penalty(reliability_score)
    )
    return round(clamp(score), 1)


def personalise_stress_score(
    base_stress: float,
    weights: Dict[str, int],
    duration_min: float,
    reliability_score: float,
) -> float:
    """
    Personalises the route score based on user preference weighting.
    Lower final score = better route.
    """
    speed_weight = weights.get("speed", 30) / 100
    stress_weight = weights.get("stress", 50) / 100
    reliability_weight = weights.get("reliability", 20) / 100

    duration_component = min(duration_min, 90) / 90 * 100
    reliability_component = 100 - clamp(reliability_score, 0, 100)

    personalised = (
        stress_weight * base_stress
        + speed_weight * duration_component
        + reliability_weight * reliability_component
    )

    return round(clamp(personalised), 1)


def interpret_stress_level(score: float) -> str:
    if score >= 70:
        return "High"
    if score >= 40:
        return "Moderate"
    return "Low"