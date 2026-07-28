from typing import Any, Dict, List

from bs4 import BeautifulSoup


def _extract_headings(
    soup: BeautifulSoup,
    tag_name: str,
) -> List[str]:
    headings = []

    for tag in soup.find_all(tag_name):
        text = tag.get_text(
            " ",
            strip=True,
        )

        if text:
            headings.append(text)

    return headings


def analyze_headings(
    soup: BeautifulSoup,
    keyword: str | None = None,
) -> Dict[str, Any]:
    h1 = _extract_headings(soup, "h1")
    h2 = _extract_headings(soup, "h2")
    h3 = _extract_headings(soup, "h3")

    keyword_in_h1 = None

    if keyword:
        keyword_in_h1 = any(
            keyword.lower() in heading.lower()
            for heading in h1
        )

    return {
        "h1": {
            "count": len(h1),
            "items": h1,
            "exactly_one": len(h1) == 1,
            "keyword_present": keyword_in_h1,
        },
        "h2": {
            "count": len(h2),
            "items": h2,
        },
        "h3": {
            "count": len(h3),
            "items": h3,
        },
        "total": len(h1) + len(h2) + len(h3),
    }
