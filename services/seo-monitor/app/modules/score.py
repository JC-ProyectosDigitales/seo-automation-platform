from typing import Any, Dict, List


def _calculate_infrastructure_score(
    analysis: Dict[str, Any],
) -> int:
    score = 0

    availability = analysis["availability"]
    response_time = analysis["response_time"]
    redirects = analysis["redirects"]
    ssl_result = analysis["ssl"]

    if availability["available"]:
        score += 35

    status_code = availability.get(
        "status_code"
    )

    if (
        status_code
        and 200 <= status_code < 300
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

    if (
        ssl_result["enabled"]
        and ssl_result["valid"]
    ):
        score += 15

    if (
        ssl_result["valid"]
        and (
            ssl_result["expires_soon"]
            is False
        )
    ):
        score += 5

    return min(
        score,
        100,
    )


def _calculate_pagespeed_score(
    analysis: Dict[str, Any],
) -> int | None:
    pagespeed = analysis.get(
        "pagespeed",
        {},
    )

    if not pagespeed.get(
        "available",
        False,
    ):
        return None

    scores = pagespeed.get(
        "scores",
        {},
    )

    weighted_scores: List[
        tuple[int, float]
    ] = []

    weights = {
        "performance": 0.50,
        "accessibility": 0.15,
        "best_practices": 0.15,
        "seo": 0.20,
    }

    for category, weight in (
        weights.items()
    ):
        value = scores.get(
            category
        )

        if isinstance(
            value,
            (int, float),
        ):
            weighted_scores.append(
                (
                    int(value),
                    weight,
                )
            )

    if not weighted_scores:
        return None

    total_weight = sum(
        weight
        for _, weight
        in weighted_scores
    )

    weighted_total = sum(
        value * weight
        for value, weight
        in weighted_scores
    )

    return round(
        weighted_total / total_weight
    )


def calculate_score(
    analysis: Dict[str, Any],
) -> int:
    infrastructure_score = (
        _calculate_infrastructure_score(
            analysis
        )
    )

    pagespeed_score = (
        _calculate_pagespeed_score(
            analysis
        )
    )

    if pagespeed_score is None:
        return infrastructure_score

    final_score = round(
        infrastructure_score * 0.40
        + pagespeed_score * 0.60
    )

    return max(
        0,
        min(final_score, 100),
    )
