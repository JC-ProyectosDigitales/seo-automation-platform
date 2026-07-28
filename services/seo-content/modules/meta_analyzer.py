from typing import Any, Dict, List

from bs4 import BeautifulSoup


def analyze_meta(
    html: str,
    keyword: str,
) -> Dict[str, Any]:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = ""

    if soup.title and soup.title.string:
        title = " ".join(
            soup.title.string.split()
        )

    description = ""

    description_tag = soup.find(
        "meta",
        attrs={
            "name": lambda value: (
                value
                and value.lower() == "description"
            )
        },
    )

    if description_tag:
        description = " ".join(
            description_tag.get(
                "content",
                "",
            ).split()
        )

    title_length = len(
        title
    )

    description_length = len(
        description
    )

    keyword_lower = keyword.lower()

    title_keyword_present = (
        keyword_lower in title.lower()
        if title
        else False
    )

    description_keyword_present = (
        keyword_lower in description.lower()
        if description
        else False
    )

    recommendations: List[str] = []

    if not title:
        recommendations.append(
            "Agrega un título SEO."
        )

    elif not 30 <= title_length <= 60:
        recommendations.append(
            "Mantén el título SEO entre 30 y 60 caracteres."
        )

    if title and not title_keyword_present:
        recommendations.append(
            "Incluye la palabra clave en el título SEO."
        )

    if not description:
        recommendations.append(
            "Agrega una Meta Description."
        )

    elif not 120 <= description_length <= 160:
        recommendations.append(
            "Mantén la Meta Description entre 120 y 160 caracteres."
        )

    if (
        description
        and not description_keyword_present
    ):
        recommendations.append(
            "Incluye la palabra clave en la Meta Description."
        )

    return {
        "title": {
            "exists": bool(title),
            "text": title,
            "length": title_length,
            "optimal_length": (
                30 <= title_length <= 60
            ),
            "keyword_present": title_keyword_present,
            "recommended_min": 30,
            "recommended_max": 60,
        },
        "description": {
            "exists": bool(description),
            "text": description,
            "length": description_length,
            "optimal_length": (
                120 <= description_length <= 160
            ),
            "keyword_present": (
                description_keyword_present
            ),
            "recommended_min": 120,
            "recommended_max": 160,
        },
        "recommendations": recommendations,
    }
