from typing import Any, Dict, List


def optimize_content(
    seo_result: Dict[str, Any],
    heading_result: Dict[str, Any],
    readability_result: Dict[str, Any],
    meta_result: Dict[str, Any],
) -> Dict[str, Any]:
    keyword = seo_result["keyword"]

    optimization_tips: List[str] = []

    suggested_title = (
        f"{keyword.title()}: Guía Completa y Mejores Prácticas"
    )

    suggested_h1 = (
        f"Guía completa sobre {keyword}"
    )

    suggested_meta = (
        f"Descubre qué es {keyword}, cómo funciona y cuáles son "
        f"sus principales beneficios, estrategias y mejores prácticas."
    )

    if seo_result["density"] < 1:
        optimization_tips.append(
            "Incrementa de forma natural la presencia de la palabra clave principal."
        )

    elif seo_result["density"] > 3:
        optimization_tips.append(
            "Reduce el uso repetitivo de la palabra clave principal."
        )

    if not heading_result["h1"]["exactly_one"]:
        optimization_tips.append(
            "Utiliza exactamente una etiqueta H1."
        )

    if not heading_result["h1"]["keyword_present"]:
        optimization_tips.append(
            "Incluye la palabra clave principal en el H1."
        )

    if heading_result["h2"]["count"] == 0:
        optimization_tips.append(
            "Agrega subtítulos H2 para organizar el contenido."
        )

    if readability_result["reading_score"] < 60:
        optimization_tips.append(
            "Simplifica las oraciones para mejorar la legibilidad."
        )

    if readability_result["word_count"] < 300:
        optimization_tips.append(
            "Amplía el contenido con información relevante y útil."
        )

    if not meta_result["title"]["optimal_length"]:
        optimization_tips.append(
            "Ajusta el título SEO al rango recomendado."
        )

    if not meta_result["description"]["optimal_length"]:
        optimization_tips.append(
            "Ajusta la Meta Description al rango recomendado."
        )

    return {
        "suggested_title": suggested_title,
        "suggested_h1": suggested_h1,
        "suggested_meta_description": suggested_meta,
        "optimization_tips": list(
            dict.fromkeys(
                optimization_tips
            )
        ),
    }
