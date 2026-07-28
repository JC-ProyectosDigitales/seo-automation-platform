from typing import Any, Dict, List, Tuple


def build_issues_and_recommendations(
    analysis: Dict[str, Any],
) -> Tuple[List[Dict[str, str]], List[str]]:
    issues: List[Dict[str, str]] = []
    recommendations: List[str] = []

    title = analysis["title"]
    meta_description = analysis["meta_description"]
    headings = analysis["headings"]
    images = analysis["images"]
    links = analysis["links"]
    canonical = analysis["canonical"]
    open_graph = analysis["open_graph"]

    if not title["exists"]:
        issues.append(
            {
                "type": "error",
                "code": "TITLE_MISSING",
                "message": "La página no contiene una etiqueta title.",
            }
        )
        recommendations.append(
            "Agrega una etiqueta title descriptiva a la página."
        )

    elif not title["optimal_length"]:
        issues.append(
            {
                "type": "warning",
                "code": "TITLE_LENGTH",
                "message": (
                    "La longitud del title está fuera del rango recomendado."
                ),
            }
        )
        recommendations.append(
            "Mantén el title aproximadamente entre 30 y 60 caracteres."
        )

    if title["keyword_present"] is False:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_MISSING_IN_TITLE",
                "message": (
                    "La palabra clave no aparece en el title."
                ),
            }
        )
        recommendations.append(
            "Incluye la palabra clave principal en el title de forma natural."
        )

    if not meta_description["exists"]:
        issues.append(
            {
                "type": "error",
                "code": "META_DESCRIPTION_MISSING",
                "message": (
                    "La página no contiene una Meta Description."
                ),
            }
        )
        recommendations.append(
            "Agrega una Meta Description que resuma el contenido de la página."
        )

    elif not meta_description["optimal_length"]:
        issues.append(
            {
                "type": "warning",
                "code": "META_DESCRIPTION_LENGTH",
                "message": (
                    "La longitud de la Meta Description está fuera del rango recomendado."
                ),
            }
        )
        recommendations.append(
            "Mantén la Meta Description aproximadamente entre 120 y 160 caracteres."
        )

    if meta_description["keyword_present"] is False:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_MISSING_IN_DESCRIPTION",
                "message": (
                    "La palabra clave no aparece en la Meta Description."
                ),
            }
        )
        recommendations.append(
            "Incluye la palabra clave principal en la Meta Description."
        )

    if headings["h1"]["count"] == 0:
        issues.append(
            {
                "type": "error",
                "code": "H1_MISSING",
                "message": "La página no contiene una etiqueta H1.",
            }
        )
        recommendations.append(
            "Agrega una etiqueta H1 principal."
        )

    elif headings["h1"]["count"] > 1:
        issues.append(
            {
                "type": "warning",
                "code": "MULTIPLE_H1",
                "message": (
                    "La página contiene más de una etiqueta H1."
                ),
            }
        )
        recommendations.append(
            "Mantén una sola etiqueta H1 principal."
        )

    if headings["h1"]["keyword_present"] is False:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_MISSING_IN_H1",
                "message": (
                    "La palabra clave no aparece en el H1."
                ),
            }
        )
        recommendations.append(
            "Incluye la palabra clave principal en el H1 de forma natural."
        )

    if headings["h2"]["count"] == 0:
        issues.append(
            {
                "type": "info",
                "code": "H2_MISSING",
                "message": (
                    "No se encontraron encabezados H2."
                ),
            }
        )
        recommendations.append(
            "Usa encabezados H2 para organizar las secciones del contenido."
        )

    if images["missing_alt"] > 0:
        issues.append(
            {
                "type": "warning",
                "code": "IMAGE_ALT_MISSING",
                "message": (
                    f"{images['missing_alt']} imágenes no contienen atributo ALT."
                ),
            }
        )
        recommendations.append(
            "Agrega atributos ALT descriptivos a las imágenes relevantes."
        )

    if links["internal"]["count"] == 0:
        issues.append(
            {
                "type": "info",
                "code": "INTERNAL_LINKS_MISSING",
                "message": (
                    "No se encontraron enlaces internos."
                ),
            }
        )
        recommendations.append(
            "Agrega enlaces internos hacia otras páginas relacionadas del sitio."
        )

    if not canonical["exists"]:
        issues.append(
            {
                "type": "warning",
                "code": "CANONICAL_MISSING",
                "message": (
                    "No se encontró una etiqueta canonical."
                ),
            }
        )
        recommendations.append(
            "Agrega una etiqueta canonical para definir la URL preferida."
        )

    if not open_graph["complete"]:
        issues.append(
            {
                "type": "info",
                "code": "OPEN_GRAPH_INCOMPLETE",
                "message": (
                    "Las etiquetas Open Graph están incompletas."
                ),
            }
        )
        recommendations.append(
            "Agrega las propiedades og:title, og:description, og:image y og:url."
        )

    return issues, recommendations
