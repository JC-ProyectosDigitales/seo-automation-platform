import re

def validate_headings(content):

    h1_tags = re.findall(r'<h1.*?>(.*?)</h1>', content, re.IGNORECASE)
    h2_tags = re.findall(r'<h2.*?>(.*?)</h2>', content, re.IGNORECASE)
    h3_tags = re.findall(r'<h3.*?>(.*?)</h3>', content, re.IGNORECASE)

    recommendations = []

    # Validar H1
    if len(h1_tags) == 0:
        recommendations.append("No se encontró ninguna etiqueta H1.")
    elif len(h1_tags) > 1:
        recommendations.append("Se encontraron múltiples etiquetas H1.")
    else:
        recommendations.append("La estructura H1 es correcta.")

    # Validar H2
    if len(h2_tags) == 0:
        recommendations.append("Se recomienda agregar encabezados H2.")

    # Validar H3
    if len(h3_tags) == 0:
        recommendations.append("No se encontraron encabezados H3.")

    return {
        "h1_count": len(h1_tags),
        "h2_count": len(h2_tags),
        "h3_count": len(h3_tags),
        "recommendations": recommendations
    }