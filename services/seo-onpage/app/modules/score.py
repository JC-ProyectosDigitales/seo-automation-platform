from typing import Any, Dict


def calculate_score(
    analysis: Dict[str, Any],
) -> int:
    score = 0

    title = analysis["title"]
    meta_description = analysis["meta_description"]
    headings = analysis["headings"]
    images = analysis["images"]
    links = analysis["links"]
    canonical = analysis["canonical"]
    open_graph = analysis["open_graph"]

    if title["exists"]:
        score += 10

    if title["optimal_length"]:
        score += 10

    if title["keyword_present"] is True:
        score += 5

    if meta_description["exists"]:
        score += 10

    if meta_description["optimal_length"]:
        score += 10

    if meta_description["keyword_present"] is True:
        score += 5

    if headings["h1"]["exactly_one"]:
        score += 15

    if headings["h1"]["keyword_present"] is True:
        score += 5

    if headings["h2"]["count"] > 0:
        score += 5

    if images["missing_alt"] == 0:
        score += 10

    if links["internal"]["count"] > 0:
        score += 5

    if canonical["exists"]:
        score += 5

    if open_graph["complete"]:
        score += 5

    return min(
        score,
        100,
    )
