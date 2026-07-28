from typing import Any, Dict


def calculate_seo_score(
    seo_result: Dict[str, Any],
    heading_result: Dict[str, Any],
    readability_result: Dict[str, Any],
    meta_result: Dict[str, Any],
) -> int:
    score = 0

    density = seo_result["density"]

    if 1 <= density <= 3:
        score += 25

    elif 0 < density < 1:
        score += 12

    elif 3 < density <= 5:
        score += 10

    if heading_result["h1"]["exactly_one"]:
        score += 10

    if heading_result["h1"]["keyword_present"]:
        score += 5

    if heading_result["h2"]["count"] > 0:
        score += 5

    reading_score = readability_result[
        "reading_score"
    ]

    if reading_score >= 60:
        score += 20

    elif reading_score >= 40:
        score += 10

    word_count = readability_result[
        "word_count"
    ]

    if word_count >= 600:
        score += 10

    elif word_count >= 300:
        score += 7

    elif word_count >= 150:
        score += 3

    if meta_result["title"]["optimal_length"]:
        score += 10

    elif meta_result["title"]["exists"]:
        score += 5

    if meta_result["description"]["optimal_length"]:
        score += 10

    elif meta_result["description"]["exists"]:
        score += 5

    if meta_result["title"]["keyword_present"]:
        score += 3

    if meta_result["description"]["keyword_present"]:
        score += 2

    return min(
        score,
        100,
    )
