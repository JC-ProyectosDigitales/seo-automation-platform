from modules.keyword_analyzer import analyze_keyword
from modules.heading_validator import validate_headings
from modules.readability import analyze_readability
from modules.meta_analyzer import analyze_meta
from modules.faq_generator import generate_faqs
from modules.keyword_suggestions import generate_keyword_suggestions
from modules.seo_optimizer import optimize_content
from modules.seo_score import calculate_seo_score


def execute(audit_id, keyword, content):

    seo_result = analyze_keyword(content, keyword)

    heading_result = validate_headings(content)

    readability_result = analyze_readability(content)

    meta_result = analyze_meta(content)

    faq_result = generate_faqs(content, keyword)

    keyword_suggestions = generate_keyword_suggestions(keyword)

    optimization_result = optimize_content(
        seo_result,
        heading_result,
        readability_result,
        meta_result
    )

    seo_score = calculate_seo_score(
        seo_result,
        heading_result,
        readability_result
    )

    issues = []

    if seo_result["density"] < 1:
        issues.append({
            "type": "warning",
            "message": "La palabra clave aparece muy pocas veces."
        })

    if heading_result["h1_count"] != 1:
        issues.append({
            "type": "warning",
            "message": "Debe existir exactamente un H1."
        })

    if readability_result["reading_score"] < 60:
        issues.append({
            "type": "warning",
            "message": "La legibilidad puede mejorar."
        })

    return {
        "success": True,
        "module": "seo-content",
        "audit_id": audit_id,
        "status": "completed",
        "score": seo_score,
        "analysis": {
            "word_count": readability_result["word_count"],
            "keyword_density": seo_result["density"],
            "readability": readability_result["reading_score"]
        },
        "issues": issues,
        "recommendations": optimization_result["optimization_tips"]
    }