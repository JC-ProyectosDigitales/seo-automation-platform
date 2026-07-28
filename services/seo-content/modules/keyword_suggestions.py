from typing import Any, Dict, List


def generate_keyword_suggestions(
    keyword: str,
) -> Dict[str, Any]:
    normalized_keyword = " ".join(
        keyword.strip().lower().split()
    )

    suggestions: List[str] = [
        f"{normalized_keyword} para principiantes",
        f"guía completa de {normalized_keyword}",
        f"mejores prácticas de {normalized_keyword}",
        f"estrategias de {normalized_keyword}",
        f"herramientas para {normalized_keyword}",
        f"beneficios de {normalized_keyword}",
        f"cómo mejorar {normalized_keyword}",
        f"tendencias de {normalized_keyword}",
        f"ejemplos de {normalized_keyword}",
        f"consejos sobre {normalized_keyword}",
    ]

    return {
        "keyword": normalized_keyword,
        "total": len(suggestions),
        "suggestions": suggestions,
    }
