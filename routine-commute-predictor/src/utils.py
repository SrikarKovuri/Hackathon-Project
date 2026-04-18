from __future__ import annotations

from datetime import datetime
from typing import Dict, List


def parse_time_to_minutes(time_str: str) -> int:
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.hour * 60 + dt.minute
    except ValueError:
        return 0


def minutes_to_time_str(total_minutes: int) -> str:
    total_minutes = max(0, total_minutes)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def add_minutes_to_time(time_str: str, minutes_to_add: int) -> str:
    total = parse_time_to_minutes(time_str) + minutes_to_add
    return minutes_to_time_str(total)


def format_route_summary(route: Dict) -> str:
    return (
        f"{route.get('name', 'Route')} · "
        f"{route.get('duration', '?')} min · "
        f"{route.get('transfers', '?')} transfers · "
        f"Stress {route.get('stress', '?')}/100"
    )


def top_n_routes_by_lowest_stress(route_options: List[Dict], n: int = 3) -> List[Dict]:
    return sorted(route_options, key=lambda x: x.get("stress", 100))[:n]


def safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default