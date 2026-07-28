def generate_issues(result: dict) -> list[dict]:

    issues = []

    https = result.get("https", {})
    http_status = result.get("http_status", {})
    response_time = result.get("response_time", {})
    robots = result.get("robots", {})
    sitemap = result.get("sitemap", {})
    redirect = result.get("redirect", {})
    canonical = result.get("canonical", {})
    meta_robots = result.get("meta_robots", {})

    if not https.get("secure"):
        issues.append({
            "type": "error",
            "code": "HTTPS_MISSING",
            "message": "El sitio no utiliza HTTPS."
        })

    if not http_status.get("success"):
        issues.append({
            "type": "error",
            "code": "HTTP_STATUS_INVALID",
            "message": "La página no devuelve un estado HTTP exitoso."
        })

    measured_time = response_time.get("response_time")

    if measured_time is None:
        issues.append({
            "type": "warning",
            "code": "RESPONSE_TIME_UNAVAILABLE",
            "message": "No fue posible medir el tiempo de respuesta."
        })
    elif measured_time >= 1000:
        issues.append({
            "type": "warning",
            "code": "RESPONSE_TIME_HIGH",
            "message": "El tiempo de respuesta supera los 1000 ms."
        })

    if not robots.get("exists"):
        issues.append({
            "type": "warning",
            "code": "ROBOTS_MISSING",
            "message": "No se encontró el archivo robots.txt."
        })
    else:
        if not robots.get("has_user_agent"):
            issues.append({
                "type": "warning",
                "code": "ROBOTS_USER_AGENT_MISSING",
                "message": "robots.txt no contiene una directiva User-agent."
            })

        if not robots.get("has_sitemap"):
            issues.append({
                "type": "warning",
                "code": "ROBOTS_SITEMAP_MISSING",
                "message": "robots.txt no contiene una referencia al sitemap."
            })

    if not sitemap.get("exists"):
        issues.append({
            "type": "warning",
            "code": "SITEMAP_MISSING",
            "message": "No se encontró el archivo sitemap.xml."
        })
    elif not sitemap.get("valid_xml"):
        issues.append({
            "type": "error",
            "code": "SITEMAP_INVALID_XML",
            "message": "El sitemap existe, pero su contenido XML no es válido."
        })

    redirect_statuses = {
        redirect.get("www_status"),
        redirect.get("non_www_status")
    }

    if 301 not in redirect_statuses and 308 not in redirect_statuses:
        issues.append({
            "type": "warning",
            "code": "WWW_REDIRECT_MISSING",
            "message": "No se detectó una redirección permanente entre WWW y no WWW."
        })

    if not canonical.get("exists"):
        issues.append({
            "type": "warning",
            "code": "CANONICAL_MISSING",
            "message": "No se encontró una etiqueta canonical."
        })

    if not meta_robots.get("exists"):
        issues.append({
            "type": "info",
            "code": "META_ROBOTS_MISSING",
            "message": "No se encontró una etiqueta meta robots."
        })
    else:
        if meta_robots.get("index") is False:
            issues.append({
                "type": "warning",
                "code": "META_ROBOTS_NOINDEX",
                "message": "La página está configurada con la directiva noindex."
            })

        if meta_robots.get("follow") is False:
            issues.append({
                "type": "warning",
                "code": "META_ROBOTS_NOFOLLOW",
                "message": "La página está configurada con la directiva nofollow."
            })

    return issues
