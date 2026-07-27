import re

def analyze_keyword(content, keyword):

    content_lower = content.lower()
    keyword_lower = keyword.lower()

    words = re.findall(r'\w+', content_lower)

    total_words = len(words)

    keyword_count = words.count(keyword_lower)

    if total_words > 0:
        density = (keyword_count / total_words) * 100
    else:
        density = 0

    # Evaluación SEO
    if density == 0:
        recommendation = "La keyword no aparece en el contenido."
    elif density < 1:
        recommendation = "La keyword aparece muy poco."
    elif density <= 3:
        recommendation = "La densidad SEO es adecuada."
    elif density <= 6:
        recommendation = "La keyword aparece demasiadas veces."
    else:
        recommendation = "Posible keyword stuffing detectado."

    return {
        "keyword": keyword,
        "keyword_count": keyword_count,
        "total_words": total_words,
        "density": round(density, 2),
        "recommendation": recommendation
    }


