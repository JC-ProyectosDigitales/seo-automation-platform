def optimize_content(
    seo_result,
    heading_result,
    readability_result,
    meta_result
):

    keyword = seo_result["keyword"]

    optimization_tips = []

    # Título sugerido

    suggested_title = (
        f"{keyword.title()} | Guía Completa y Mejores Prácticas"
    )

    # H1 sugerido

    suggested_h1 = (
        f"Guía Completa sobre {keyword.title()}"
    )

    # Meta Description sugerida

    suggested_meta = (
        f"Descubre todo sobre {keyword}. "
        f"Aprende estrategias, consejos y mejores prácticas "
        f"para mejorar tus resultados."
    )

    # Keyword

    if seo_result["density"] < 1:
        optimization_tips.append(
            "Incrementar la presencia de la keyword principal."
        )

    # H1

    if heading_result["h1_count"] != 1:
        optimization_tips.append(
            "Mantener una única etiqueta H1."
        )

    # H2

    if heading_result["h2_count"] == 0:
        optimization_tips.append(
            "Agregar subtítulos H2 para mejorar la estructura."
        )

    # Legibilidad

    if readability_result["reading_score"] < 60:
        optimization_tips.append(
            "Reducir la longitud de las oraciones."
        )

    # Meta Description

    if meta_result["description_length"] < 120:
        optimization_tips.append(
            "Ampliar la Meta Description."
        )

    return {
        "suggested_title": suggested_title,
        "suggested_h1": suggested_h1,
        "suggested_meta": suggested_meta,
        "optimization_tips": optimization_tips
    }