import re
from typing import Any, Dict


def analyze_keyword(
    content: str,
    keyword: str,
) -> Dict[str, Any]:
    normalized_content = " ".join(
        content.lower().split()
    )

    normalized_keyword = " ".join(
        keyword.lower().split()
    )

    words = re.findall(
        r"\b[\wáéíóúüñ]+\b",
        normalized_content,
        flags=re.UNICODE,
    )

    total_words = len(words)

    keyword_pattern = re.compile(
        rf"(?<!\w){re.escape(normalized_keyword)}(?!\w)",
        flags=re.IGNORECASE,
    )

    keyword_count = len(
        keyword_pattern.findall(
            normalized_content
        )
    )

    keyword_word_count = max(
        len(normalized_keyword.split()),
        1,
    )

    density = 0.0

    if total_words > 0:
        density = (
            keyword_count
            * keyword_word_count
            / total_words
        ) * 100

    density = round(
        density,
        2,
    )

    if density == 0:
        rating = "missing"
        recommendation = (
            "La palabra clave no aparece en el contenido."
        )

    elif density < 1:
        rating = "low"
        recommendation = (
            "La palabra clave aparece con poca frecuencia."
        )

    elif density <= 3:
        rating = "optimal"
        recommendation = (
            "La densidad de la palabra clave es adecuada."
        )

    elif density <= 5:
        rating = "high"
        recommendation = (
            "La palabra clave aparece con demasiada frecuencia."
        )

    else:
        rating = "stuffing"
        recommendation = (
            "Se detectó posible uso excesivo de la palabra clave."
        )

    return {
        "keyword": keyword,
        "normalized_keyword": normalized_keyword,
        "keyword_count": keyword_count,
        "total_words": total_words,
        "density": density,
        "rating": rating,
        "recommended_min": 1,
        "recommended_max": 3,
        "recommendation": recommendation,
    }
