from typing import Any, Dict

from bs4 import BeautifulSoup


REQUIRED_PROPERTIES = (
    "og:title",
    "og:description",
    "og:image",
    "og:url",
)


def analyze_open_graph(
    soup: BeautifulSoup,
) -> Dict[str, Any]:
    properties: Dict[str, str] = {}

    for meta_tag in soup.find_all("meta"):
        property_name = meta_tag.get(
            "property",
            "",
        ).strip().lower()

        if not property_name.startswith("og:"):
            continue

        content = meta_tag.get(
            "content",
            "",
        ).strip()

        if content:
            properties[property_name] = content

    missing = [
        property_name
        for property_name in REQUIRED_PROPERTIES
        if property_name not in properties
    ]

    return {
        "exists": bool(properties),
        "complete": not missing,
        "properties": properties,
        "missing_properties": missing,
    }
