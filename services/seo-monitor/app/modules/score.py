from typing import Any, Dict


def calculate_score(
    analysis: Dict[str, Any],
) -> int:
    score = 0

    availability = analysis["availability"]
    response_time = analysis["response_time"]
    redirects = analysis["redirects"]
    ssl_result = analysis["ssl"]

    if availability["available"]:
        score += 40

    if (
        availability["status_code"]
        and 200
        <= availability["status_code"]
        < 300
    ):
        score += 15

    if response_time["rating"] == "excellent":
        score += 20

    elif response_time["rating"] == "good":
        score += 15

    elif response_time["rating"] == "acceptable":
        score += 10

    if not redirects["has_redirects"]:
        score += 10

    elif not redirects["excessive"]:
        score += 5

    if ssl_result["enabled"] and ssl_result["valid"]:
        score += 15

    if (
        ssl_result["valid"]
        and ssl_result["expires_soon"] is False
    ):
        score += 5

    return min(
        score,
        100,
    )
