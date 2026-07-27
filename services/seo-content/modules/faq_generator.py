import re

def generate_faqs(content, keyword):

    content_lower = content.lower()
    keyword_lower = keyword.lower()

    faqs = []

    # FAQ base (reglas simples)
    faqs.append(f"¿Qué es {keyword}?")
    faqs.append(f"¿Para qué sirve {keyword}?")
    faqs.append(f"¿Cómo funciona {keyword}?")
    faqs.append(f"¿Por qué es importante {keyword}?")

    # Detectar contexto del contenido para FAQs más específicas
    if "seo" in content_lower:
        faqs.append("¿Cómo mejorar el SEO de una página web?")
        faqs.append("¿Cuáles son las mejores prácticas de SEO?")

    if "contenido" in content_lower:
        faqs.append("¿Cómo crear contenido optimizado para SEO?")

    if "google" in content_lower:
        faqs.append("¿Cómo posicionar en Google más rápido?")

    # Limitar duplicados
    faqs = list(dict.fromkeys(faqs))

    return {
        "keyword": keyword,
        "faqs": faqs,
        "total": len(faqs)
    }