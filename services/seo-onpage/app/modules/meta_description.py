from typing import Any, Dict

from bs4 import BeautifulSoup


def analyze_meta_description(
    soup: BeautifulSoup,
    keyword: str | None = None,
) -> Dict[str, Any]:
    meta_tag = soup.find(
        "meta",
        attrs={"name": lambda value: value and value.lower() == "description"},
    )

    description = ""

    if meta_tag:
        description = meta_tag.get(
            "content",
            "",
        ).strip()

    length = len(description)

    keyword_present = None

    if keyword:
        keyword_present = (
            keyword.lower() in description.lower()
        )

    return {
        "exists": bool(description),
        "content": description or None,
        "length": length,
        "recommended_min": 120,
        "recommended_max": 160,
        "optimal_length": 120 <= length <= 160,
        "keyword_present": keyword_present,
    }
