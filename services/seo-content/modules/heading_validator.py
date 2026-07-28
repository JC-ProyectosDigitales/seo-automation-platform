from typing import Any, Dict, List

from bs4 import BeautifulSoup


def _clean_text(value: str) -> str:
    return " ".join(
        value.split()
    )


def validate_headings(
    html: str,
    keyword: str,
) -> Dict[str, Any]:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    h1_items: List[str] = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in soup.find_all("h1")
    ]

    h2_items: List[str] = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in soup.find_all("h2")
    ]

    h3_items: List[str] = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in soup.find_all("h3")
    ]

    keyword_lower = keyword.lower()

    h1_keyword_present = any(
        keyword_lower in item.lower()
        for item in h1_items
    )

    recommendations: List[str] = []

    if len(h1_items) == 0:
        recommendations.append(
            "Agrega una etiqueta H1 principal."
        )

    elif len(h1_items) > 1:
        recommendations.append(
            "Mantén una sola etiqueta H1 principal."
        )

    if h1_items and not h1_keyword_present:
        recommendations.append(
            "Incluye la palabra clave principal en el H1."
        )

    if len(h2_items) == 0:
        recommendations.append(
            "Agrega encabezados H2 para organizar las secciones."
        )

    if len(h3_items) == 0:
        recommendations.append(
            "Considera usar encabezados H3 para subsecciones."
        )

    return {
        "h1": {
            "count": len(h1_items),
            "items": h1_items,
            "exactly_one": len(h1_items) == 1,
            "keyword_present": h1_keyword_present,
        },
        "h2": {
            "count": len(h2_items),
            "items": h2_items,
        },
        "h3": {
            "count": len(h3_items),
            "items": h3_items,
        },
        "total": (
            len(h1_items)
            + len(h2_items)
            + len(h3_items)
        ),
        "recommendations": recommendations,
    }
