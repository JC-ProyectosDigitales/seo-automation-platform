def generate_keyword_suggestions(keyword):

    keyword = keyword.strip().lower()

    suggestions = [
        f"{keyword} para principiantes",
        f"guía completa de {keyword}",
        f"mejores prácticas de {keyword}",
        f"estrategias de {keyword}",
        f"herramientas para {keyword}",
        f"beneficios de {keyword}",
        f"cómo mejorar {keyword}",
        f"tendencias de {keyword}",
        f"ejemplos de {keyword}",
        f"consejos sobre {keyword}"
    ]

    return {
        "keyword": keyword,
        "total": len(suggestions),
        "suggestions": suggestions
    }