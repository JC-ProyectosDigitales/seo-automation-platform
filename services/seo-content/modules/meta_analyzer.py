import re

def analyze_meta(content):

    recommendations = []

    title_match = re.search(
        r'<title>(.*?)</title>',
        content,
        re.IGNORECASE | re.DOTALL
    )

    meta_match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        content,
        re.IGNORECASE
    )

    title = title_match.group(1).strip() if title_match else ""

    description = (
        meta_match.group(1).strip()
        if meta_match else ""
    )

    title_length = len(title)

    description_length = len(description)

    # Validación título

    if not title:
        recommendations.append(
            "No se encontró etiqueta TITLE."
        )

    elif title_length < 30:
        recommendations.append(
            "El título SEO es demasiado corto."
        )

    elif title_length > 60:
        recommendations.append(
            "El título SEO supera los 60 caracteres."
        )

    else:
        recommendations.append(
            "La longitud del título SEO es adecuada."
        )

    # Validación meta description

    if not description:
        recommendations.append(
            "No se encontró Meta Description."
        )

    elif description_length < 120:
        recommendations.append(
            "La Meta Description es demasiado corta."
        )

    elif description_length > 160:
        recommendations.append(
            "La Meta Description supera los 160 caracteres."
        )

    else:
        recommendations.append(
            "La Meta Description tiene una longitud adecuada."
        )

    return {
        "title": title,
        "title_length": title_length,
        "description": description,
        "description_length": description_length,
        "recommendations": recommendations
    }