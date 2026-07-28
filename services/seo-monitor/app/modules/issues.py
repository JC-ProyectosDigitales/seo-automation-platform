from typing import Any, Dict, List, Tuple


def build_issues_and_recommendations(
    analysis: Dict[str, Any],
) -> Tuple[List[Dict[str, str]], List[str]]:
    issues: List[Dict[str, str]] = []
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
                    "El sitio web no está disponible."
                ),
            }
        )
        recommendations.append(
            "Verifica el servidor, el dominio y la conectividad del sitio."
        )

    elif availability["status_code"] and (
        availability["status_code"] >= 400
    ):
        issues.append(
            {
                "type": "error",
                "code": "INVALID_HTTP_STATUS",
                "message": (
                    "El sitio devolvió el código HTTP "
                    f"{availability['status_code']}."
                ),
            }
        )
        recommendations.append(
            "Corrige el error HTTP devuelto por la URL auditada."
        )

    if not response_time["acceptable"]:
        issues.append(
            {
                "type": "warning",
                "code": "SLOW_RESPONSE_TIME",
                "message": (
                    "El tiempo de respuesta supera los "
                    "2000 milisegundos recomendados."
                ),
            }
        )
        recommendations.append(
            "Optimiza el servidor, caché y recursos para reducir el tiempo de respuesta."
        )

    elif response_time["rating"] == "acceptable":
        issues.append(
            {
                "type": "info",
                "code": "RESPONSE_TIME_IMPROVABLE",
                "message": (
                    "El tiempo de respuesta es aceptable, "
                    "pero puede mejorar."
                ),
            }
        )
        recommendations.append(
            "Intenta mantener el tiempo de respuesta por debajo de 1000 milisegundos."
        )

    if redirects["excessive"]:
        issues.append(
            {
                "type": "warning",
                "code": "EXCESSIVE_REDIRECTS",
                "message": (
                    "La URL utiliza demasiadas redirecciones."
                ),
            }
        )
        recommendations.append(
            "Reduce la cadena de redirecciones a un máximo de dos saltos."
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
            "Instala un certificado SSL y redirige todo el tráfico HTTP hacia HTTPS."
        )

    elif not ssl_result["valid"]:
        issues.append(
            {
                "type": "error",
                "code": "SSL_INVALID",
                "message": (
                    "El certificado SSL no es válido o no pudo verificarse."
                ),
            }
        )
        recommendations.append(
            "Revisa la configuración, vigencia y cadena de confianza del certificado SSL."
        )

    elif ssl_result["expires_soon"]:
        issues.append(
            {
                "type": "warning",
                "code": "SSL_EXPIRES_SOON",
                "message": (
                    "El certificado SSL vence dentro de "
                    f"{ssl_result['days_remaining']} días."
                ),
            }
        )
        recommendations.append(
            "Renueva el certificado SSL antes de su fecha de vencimiento."
        )

    return issues, recommendations
