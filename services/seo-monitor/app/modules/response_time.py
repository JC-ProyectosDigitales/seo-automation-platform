from typing import Any, Dict


def analyze_response_time(
    response_time_ms: float | None,
) -> Dict[str, Any]:
    if response_time_ms is None:
        return {
            "response_time_ms": None,
            "rating": "unavailable",
            "acceptable": False,
            "recommended_max_ms": 2000,
        }

    rating = "slow"

    if response_time_ms <= 500:
        rating = "excellent"

    elif response_time_ms <= 1000:
        rating = "good"

    elif response_time_ms <= 2000:
        rating = "acceptable"

    return {
        "response_time_ms": response_time_ms,
        "rating": rating,
        "acceptable": response_time_ms <= 2000,
        "recommended_max_ms": 2000,
    }
