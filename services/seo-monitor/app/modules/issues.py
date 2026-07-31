from typing import Any, Dict, List, Tuple


def _add_pagespeed_issues(
    analysis: Dict[str, Any],
    issues: List[Dict[str, str]],
    recommendations: List[str],
) -> None:
    pagespeed = analysis.get(
        "pagespeed",
        {},
    )

    if not pagespeed.get(
        "available",
        False,
    ):
        issues.append(
            {
                "type": "info",
                "code": (
                    "PAGESPEED_UNAVAILABLE"
                ),
                "message": (
                    "No fue posible obtener "
                    "el análisis de PageSpeed "
                    "Insights."
                ),
            }
        )

        recommendations.append(
            "Reintenta el análisis de "
            "PageSpeed Insights más tarde."
        )

        return

    scores = pagespeed.get(
        "scores",
        {},
    )

    category_settings = {
        "performance": {
            "label": "rendimiento",
            "code": (
                "PAGESPEED_PERFORMANCE_LOW"
            ),
        },
        "accessibility": {
            "label": "accesibilidad",
            "code": (
                "PAGESPEED_ACCESSIBILITY_LOW"
            ),
        },
        "best_practices": {
            "label": "mejores prácticas",
            "code": (
                "PAGESPEED_BEST_PRACTICES_LOW"
            ),
        },
        "seo": {
            "label": "SEO técnico",
            "code": "PAGESPEED_SEO_LOW",
        },
    }

    for category, settings in (
        category_settings.items()
    ):
        score = scores.get(
            category
        )

        if not isinstance(
            score,
            (int, float),
        ):
            continue

        if score < 50:
            issue_type = "error"
            qualifier = "baja"

        elif score < 90:
            issue_type = "warning"
            qualifier = "mejorable"

        else:
            continue

        issues.append(
            {
                "type": issue_type,
                "code": settings["code"],
                "message": (
                    "La puntuación de "
                    f"{settings['label']} "
                    f"es {score} y se considera "
                    f"{qualifier}."
                ),
            }
        )

        recommendations.append(
            "Revisa las recomendaciones de "
            "Lighthouse para mejorar "
            f"{settings['label']}."
        )

    metrics = pagespeed.get(
        "metrics",
        {},
    )

    metric_settings = {
        "largest_contentful_paint": {
            "label": (
                "Largest Contentful Paint"
            ),
            "code": "LCP_IMPROVABLE",
            "recommendation": (
                "Optimiza imágenes, recursos "
                "críticos y tiempo de respuesta "
                "para mejorar el LCP."
            ),
        },
        "cumulative_layout_shift": {
            "label": (
                "Cumulative Layout Shift"
            ),
            "code": "CLS_IMPROVABLE",
            "recommendation": (
                "Define dimensiones para "
                "imágenes y elementos dinámicos "
                "para reducir cambios de diseño."
            ),
        },
        "interaction_to_next_paint": {
            "label": (
                "Interaction to Next Paint"
            ),
            "code": "INP_IMPROVABLE",
            "recommendation": (
                "Reduce las tareas largas de "
                "JavaScript para mejorar la "
                "capacidad de respuesta."
            ),
        },
        "total_blocking_time": {
            "label": (
                "Total Blocking Time"
            ),
            "code": "TBT_IMPROVABLE",
            "recommendation": (
                "Divide tareas extensas y "
                "reduce JavaScript innecesario "
                "para mejorar el TBT."
            ),
        },
    }

    for metric_name, settings in (
        metric_settings.items()
    ):
        metric = metrics.get(
            metric_name,
            {},
        )

        rating = metric.get(
            "rating"
        )

        if rating not in {
            "needs_improvement",
            "poor",
        }:
            continue

        issues.append(
            {
                "type": (
                    "error"
                    if rating == "poor"
                    else "warning"
                ),
                "code": settings["code"],
                "message": (
                    f"{settings['label']} "
                    "se encuentra fuera del "
                    "rango recomendado."
                ),
            }
        )

        recommendations.append(
            settings["recommendation"]
        )

    opportunities = pagespeed.get(
        "opportunities",
        [],
    )

    for opportunity in opportunities[:5]:
        title = opportunity.get(
            "title"
        )

        if not title:
            continue

        recommendation = (
            f"PageSpeed: {title}"
        )

        display_value = opportunity.get(
            "display_value"
        )

        if display_value:
            recommendation += (
                f" ({display_value})"
            )

        recommendations.append(
            recommendation
        )


def build_issues_and_recommendations(
    analysis: Dict[str, Any],
) -> Tuple[List[Dict[str, str]], List[str]]:
    issues: List[
        Dict[str, str]
    ] = []

    recommendations: List[str] = []

    availability = analysis["availability"]
    response_time = analysis["response_time"]
    redirects = analysis["redirects"]
    ssl_result = analysis["ssl"]

    if not availability["available"]:
        issues.append(
            {
                "type": "error",
                "code": "WEBSITE_UNAVAILABLE",
                "message": (
                    "El sitio web no está "
                    "disponible."
                ),
            }
        )

        recommendations.append(
            "Verifica el servidor, el dominio "
            "y la conectividad del sitio."
        )

    elif availability["status_code"] and (
        availability["status_code"] >= 400
    ):
        issues.append(
            {
                "type": "error",
                "code": (
                    "INVALID_HTTP_STATUS"
                ),
                "message": (
                    "El sitio devolvió el código "
                    "HTTP "
                    f"{availability['status_code']}."
                ),
            }
        )

        recommendations.append(
            "Corrige el error HTTP devuelto "
            "por la URL auditada."
        )

    if not response_time["acceptable"]:
        issues.append(
            {
                "type": "warning",
                "code": (
                    "SLOW_RESPONSE_TIME"
                ),
                "message": (
                    "El tiempo de respuesta "
                    "supera los 2000 "
                    "milisegundos recomendados."
                ),
            }
        )

        recommendations.append(
            "Optimiza el servidor, caché y "
            "recursos para reducir el tiempo "
            "de respuesta."
        )

    elif (
        response_time["rating"]
        == "acceptable"
    ):
        issues.append(
            {
                "type": "info",
                "code": (
                    "RESPONSE_TIME_IMPROVABLE"
                ),
                "message": (
                    "El tiempo de respuesta es "
                    "aceptable, pero puede "
                    "mejorar."
                ),
            }
        )

        recommendations.append(
            "Intenta mantener el tiempo de "
            "respuesta por debajo de 1000 "
            "milisegundos."
        )

    if redirects["excessive"]:
        issues.append(
            {
                "type": "warning",
                "code": (
                    "EXCESSIVE_REDIRECTS"
                ),
                "message": (
                    "La URL utiliza demasiadas "
                    "redirecciones."
                ),
            }
        )

        recommendations.append(
            "Reduce la cadena de redirecciones "
            "a un máximo de dos saltos."
        )

    if not ssl_result["enabled"]:
        issues.append(
            {
                "type": "error",
                "code": "HTTPS_DISABLED",
                "message": (
                    "La URL no utiliza HTTPS."
                ),
            }
        )

        recommendations.append(
            "Instala un certificado SSL y "
            "redirige todo el tráfico HTTP "
            "hacia HTTPS."
        )

    elif not ssl_result["valid"]:
        issues.append(
            {
                "type": "error",
                "code": "SSL_INVALID",
                "message": (
                    "El certificado SSL no es "
                    "válido o no pudo "
                    "verificarse."
                ),
            }
        )

        recommendations.append(
            "Revisa la configuración, vigencia "
            "y cadena de confianza del "
            "certificado SSL."
        )

    elif ssl_result["expires_soon"]:
        issues.append(
            {
                "type": "warning",
                "code": (
                    "SSL_EXPIRES_SOON"
                ),
                "message": (
                    "El certificado SSL vence "
                    "dentro de "
                    f"{ssl_result['days_remaining']} "
                    "días."
                ),
            }
        )

        recommendations.append(
            "Renueva el certificado SSL antes "
            "de su fecha de vencimiento."
        )

    _add_pagespeed_issues(
        analysis,
        issues,
        recommendations,
    )

    recommendations = list(
        dict.fromkeys(
            recommendations
        )
    )

    return issues, recommendations
