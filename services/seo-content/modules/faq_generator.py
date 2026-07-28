from typing import Any, Dict, List


def generate_faqs(
    content: str,
    keyword: str,
) -> Dict[str, Any]:
    content_lower = content.lower()

    faqs: List[str] = [
        f"¿Qué es {keyword}?",
        f"¿Para qué sirve {keyword}?",
        f"¿Cómo funciona {keyword}?",
        f"¿Cuáles son los beneficios de {keyword}?",
    ]

    if "seo" in content_lower:
        faqs.extend(
            [
                "¿Cómo mejorar el SEO de una página web?",
                "¿Cuáles son las mejores prácticas de SEO?",
            ]
        )

    if "contenido" in content_lower:
        faqs.append(
            "¿Cómo crear contenido optimizado para SEO?"
        )

    if "google" in content_lower:
        faqs.append(
            "¿Cómo mejorar el posicionamiento en Google?"
        )

    faqs = list(
        dict.fromkeys(faqs)
    )

    return {
        "keyword": keyword,
        "total": len(faqs),
        "faqs": faqs,
    }
