from typing import Any, Dict
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


IGNORED_SCHEMES = (
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
)


def analyze_links(
    soup: BeautifulSoup,
    page_url: str,
) -> Dict[str, Any]:
    page_host = urlparse(page_url).netloc.lower()

    internal_links = []
    external_links = []
    invalid_links = []
    nofollow_links = 0

    for anchor in soup.find_all("a"):
        href = anchor.get(
            "href",
            "",
        ).strip()

        if not href:
            invalid_links.append(href)
            continue

        if href.startswith(IGNORED_SCHEMES):
            continue

        absolute_url = urljoin(
            page_url,
            href,
        )

        parsed_url = urlparse(absolute_url)

        if parsed_url.scheme not in (
            "http",
            "https",
        ):
            invalid_links.append(href)
            continue

        rel_values = anchor.get(
            "rel",
            [],
        )

        if isinstance(rel_values, str):
            rel_values = rel_values.split()

        if "nofollow" in [
            value.lower()
            for value in rel_values
        ]:
            nofollow_links += 1

        link_data = {
            "url": absolute_url,
            "text": anchor.get_text(
                " ",
                strip=True,
            ) or None,
        }

        if parsed_url.netloc.lower() == page_host:
            internal_links.append(link_data)
        else:
            external_links.append(link_data)

    return {
        "total": (
            len(internal_links)
            + len(external_links)
        ),
        "internal": {
            "count": len(internal_links),
            "links": internal_links,
        },
        "external": {
            "count": len(external_links),
            "links": external_links,
        },
        "nofollow": nofollow_links,
        "invalid": len(invalid_links),
    }
