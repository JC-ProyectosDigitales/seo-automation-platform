from typing import Any, Dict
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def analyze_canonical(
    soup: BeautifulSoup,
    page_url: str,
) -> Dict[str, Any]:
    canonical_tag = soup.find(
        "link",
        rel=lambda value: (
            value
            and "canonical" in (
                value
                if isinstance(value, list)
                else value.split()
            )
        ),
    )

    href = None

    if canonical_tag:
        raw_href = canonical_tag.get(
            "href",
            "",
        ).strip()

        if raw_href:
            href = urljoin(
                page_url,
                raw_href,
            )

    return {
        "exists": bool(href),
        "href": href,
        "matches_page": (
            href.rstrip("/") == page_url.rstrip("/")
            if href
            else None
        ),
    }
