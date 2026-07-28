def calculate_score(
    https: dict,
    http_status: dict,
    response_time: dict,
    robots: dict,
    sitemap: dict,
    redirect: dict,
    canonical: dict,
    meta_robots: dict
) -> tuple[int, list[str]]:

    score = 0
    recommendations = []

    # HTTPS: 15 puntos
    if https.get("secure"):
        score += 15
    else:
        recommendations.append(
            "Configura el sitio para utilizar HTTPS."
        )

    # Estado HTTP: 10 puntos
    if http_status.get("success"):
        score += 10
    else:
        recommendations.append(
            "Verifica que la página responda con un código HTTP exitoso."
        )

    # Tiempo de respuesta: 10 puntos
    measured_time = response_time.get("response_time")

    if measured_time is None:
        recommendations.append(
            "No fue posible medir el tiempo de respuesta del sitio."
        )
    elif measured_time < 500:
        score += 10
    elif measured_time < 1000:
        score += 5
        recommendations.append(
            "Mejora el tiempo de respuesta para mantenerlo por debajo de 500 ms."
        )
    else:
        recommendations.append(
            "El tiempo de respuesta del servidor es elevado."
        )

    # Robots.txt: 15 puntos
    if robots.get("exists"):
        score += 10

        if robots.get("has_sitemap"):
            score += 3
        else:
            recommendations.append(
                "Agrega la referencia al sitemap dentro de robots.txt."
            )

        if robots.get("has_user_agent"):
            score += 2
        else:
            recommendations.append(
                "Define al menos un User-agent dentro de robots.txt."
            )
    else:
        recommendations.append(
            "Crea y publica un archivo robots.txt."
        )

    # Sitemap: 15 puntos
    if sitemap.get("exists"):
        score += 10

        if sitemap.get("valid_xml"):
            score += 5
        else:
            recommendations.append(
                "Corrige la estructura XML del sitemap."
            )
    else:
        recommendations.append(
            "Crea y publica un archivo sitemap.xml."
        )

    # Redirecciones WWW y no WWW: 10 puntos
    redirect_statuses = {
        redirect.get("www_status"),
        redirect.get("non_www_status")
    }

    if 301 in redirect_statuses or 308 in redirect_statuses:
        score += 10
    else:
        recommendations.append(
            "Configura una redirección permanente entre las versiones WWW y no WWW."
        )

    # Canonical: 10 puntos
    if canonical.get("exists"):
        score += 10
    else:
        recommendations.append(
            "Agrega una etiqueta canonical a la página."
        )

    # Meta robots: 10 puntos
    if meta_robots.get("exists"):
        score += 10

        if meta_robots.get("index") is False:
            recommendations.append(
                "La página contiene la directiva noindex."
            )

        if meta_robots.get("follow") is False:
            recommendations.append(
                "La página contiene la directiva nofollow."
            )
    else:
        recommendations.append(
            "Agrega una etiqueta meta robots cuando necesites declarar index y follow explícitamente."
        )

    # Calidad adicional: 5 puntos
    if not recommendations:
        score += 5

    return min(score, 100), recommendations
