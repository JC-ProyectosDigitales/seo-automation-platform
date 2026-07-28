from typing import Any, Dict

from bs4 import BeautifulSoup


def analyze_title(
    soup: BeautifulSoup,
    keyword: str | None = None,
) -> Dict[str, Any]:
    title_tag = soup.find("title")

    title_text = ""

    if title_tag:
        title_text = title_tag.get_text(
            " ",
            strip=True,
        )

    length = len(title_text)

    keyword_present = None

    if keyword:
        keyword_present = (
            keyword.lower() in title_text.lower()
        )

    return {
        "exists": bool(title_text),
        "text": title_text or None,
        "length": length,
        "recommended_min": 30,
        "recommended_max": 60,
        "optimal_length": 30 <= length <= 60,
        "keyword_present": keyword_present,
    }
