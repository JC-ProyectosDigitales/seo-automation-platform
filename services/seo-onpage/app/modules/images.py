from typing import Any, Dict, List

from bs4 import BeautifulSoup


def analyze_images(
    soup: BeautifulSoup,
) -> Dict[str, Any]:
    images = soup.find_all("img")

    missing_alt: List[Dict[str, str | None]] = []
    empty_alt: List[Dict[str, str | None]] = []
    with_alt = 0

    for image in images:
        source = image.get("src")

        if not image.has_attr("alt"):
            missing_alt.append(
                {
                    "src": source,
                }
            )
            continue

        alt_text = image.get(
            "alt",
            "",
        ).strip()

        if not alt_text:
            empty_alt.append(
                {
                    "src": source,
                }
            )
            continue

        with_alt += 1

    total = len(images)

    optimized_percentage = 100.0

    if total:
        optimized_percentage = round(
            (with_alt / total) * 100,
            2,
        )

    return {
        "total": total,
        "with_alt": with_alt,
        "missing_alt": len(missing_alt),
        "empty_alt": len(empty_alt),
        "optimized_percentage": optimized_percentage,
        "missing_alt_images": missing_alt,
        "empty_alt_images": empty_alt,
    }
