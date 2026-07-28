from typing import Any, Dict, List, Tuple

from modules.faq_generator import generate_faqs
from modules.heading_validator import validate_headings
from modules.keyword_analyzer import analyze_keyword
from modules.keyword_suggestions import (
    generate_keyword_suggestions,
)
from modules.meta_analyzer import analyze_meta
from modules.readability import analyze_readability
from modules.seo_optimizer import optimize_content
from modules.seo_score import calculate_seo_score


def _build_issues(
    seo_result: Dict[str, Any],
    heading_result: Dict[str, Any],
    readability_result: Dict[str, Any],
    meta_result: Dict[str, Any],
) -> Tuple[List[Dict[str, str]], List[str]]:
    issues: List[Dict[str, str]] = []
    recommendations: List[str] = []

    if seo_result["density"] == 0:
        issues.append(
            {
                "type": "error",
                "code": "KEYWORD_MISSING",
                "message": (
                    "La palabra clave no aparece en el contenido."
                ),
            }
        )

    elif seo_result["density"] < 1:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_DENSITY_LOW",
                "message": (
                    "La densidad de la palabra clave es baja."
                ),
            }
        )

    elif seo_result["density"] > 3:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_DENSITY_HIGH",
                "message": (
                    "La densidad de la palabra clave es elevada."
                ),
            }
        )

    if heading_result["h1"]["count"] == 0:
        issues.append(
            {
                "type": "error",
                "code": "H1_MISSING",
                "message": (
                    "No se encontró una etiqueta H1."
                ),
            }
        )

    elif heading_result["h1"]["count"] > 1:
        issues.append(
            {
                "type": "warning",
                "code": "MULTIPLE_H1",
                "message": (
                    "Se encontraron múltiples etiquetas H1."
                ),
            }
        )

    if not heading_result["h1"]["keyword_present"]:
        issues.append(
            {
                "type": "warning",
                "code": "KEYWORD_MISSING_IN_H1",
                "message": (
                    "La palabra clave no aparece en el H1."
                ),
            }
        )

    if heading_result["h2"]["count"] == 0:
        issues.append(
            {
                "type": "info",
                "code": "H2_MISSING",
                "message": (
                    "No se encontraron encabezados H2."
                ),
            }
        )

    if readability_result["reading_score"] < 60:
        issues.append(
            {
                "type": "warning",
                "code": "READABILITY_LOW",
                "message": (
                    "La legibilidad del contenido puede mejorar."
                ),
            }
        )

    if readability_result["word_count"] < 300:
        issues.append(
            {
                "type": "info",
                "code": "CONTENT_SHORT",
                "message": (
                    "El contenido contiene menos de 300 palabras."
                ),
            }
        )

    if not meta_result["title"]["exists"]:
        issues.append(
            {
                "type": "error",
                "code": "TITLE_MISSING",
                "message": (
                    "No se encontró un título SEO."
                ),
            }
        )

    elif not meta_result["title"]["optimal_length"]:
        issues.append(
            {
                "type": "warning",
                "code": "TITLE_LENGTH",
                "message": (
                    "El título SEO está fuera del rango recomendado."
                ),
            }
        )

    if not meta_result["description"]["exists"]:
        issues.append(
            {
                "type": "error",
                "code": "META_DESCRIPTION_MISSING",
                "message": (
                    "No se encontró una Meta Description."
                ),
            }
        )

    elif not meta_result["description"]["optimal_length"]:
        issues.append(
            {
                "type": "warning",
                "code": "META_DESCRIPTION_LENGTH",
                "message": (
                    "La Meta Description está fuera del rango recomendado."
                ),
            }
        )

    recommendations.extend(
        [
            seo_result["recommendation"],
            *heading_result["recommendations"],
            *readability_result["recommendations"],
            *meta_result["recommendations"],
        ]
    )

    recommendations = [
        recommendation
        for recommendation in dict.fromkeys(
            recommendations
        )
        if recommendation
    ]

    return issues, recommendations


def execute(
    audit_id: str,
    website: str,
    keyword: str,
    page: Dict[str, Any],
) -> Dict[str, Any]:
    html = page["html"]
    text = page["text"]

    seo_result = analyze_keyword(
        content=text,
        keyword=keyword,
    )

    heading_result = validate_headings(
        html=html,
        keyword=keyword,
    )

    readability_result = analyze_readability(
        content=text,
    )

    meta_result = analyze_meta(
        html=html,
        keyword=keyword,
    )

    faq_result = generate_faqs(
        content=text,
        keyword=keyword,
    )

    keyword_suggestions = (
        generate_keyword_suggestions(
            keyword=keyword,
        )
    )

    optimization_result = optimize_content(
        seo_result=seo_result,
        heading_result=heading_result,
        readability_result=readability_result,
        meta_result=meta_result,
    )

    seo_score = calculate_seo_score(
        seo_result=seo_result,
        heading_result=heading_result,
        readability_result=readability_result,
        meta_result=meta_result,
    )

    issues, recommendations = _build_issues(
        seo_result=seo_result,
        heading_result=heading_result,
        readability_result=readability_result,
        meta_result=meta_result,
    )

    recommendations.extend(
        optimization_result[
            "optimization_tips"
        ]
    )

    recommendations = list(
        dict.fromkeys(
            recommendations
        )
    )

    return {
        "success": True,
        "module": "seo-content",
        "audit_id": audit_id,
        "status": "completed",
        "score": seo_score,
        "analysis": {
            "website": website,
            "keyword": keyword,
            "page": {
                "requested_url": page[
                    "requested_url"
                ],
                "final_url": page[
                    "final_url"
                ],
                "status_code": page[
                    "status_code"
                ],
                "content_type": page[
                    "content_type"
                ],
                "response_time_ms": page[
                    "response_time_ms"
                ],
                "source": page[
                    "source"
                ],
            },
            "keyword": seo_result,
            "headings": heading_result,
            "readability": readability_result,
            "meta": meta_result,
            "keyword_suggestions": (
                keyword_suggestions
            ),
            "faqs": faq_result,
            "optimization": optimization_result,
        },
        "issues": issues,
        "recommendations": recommendations,
        "errors": [],
    }
