from fastapi import APIRouter

from app.models.audit_request import AuditRequest
from app.modules.analyzer import analyze_site


router = APIRouter(
    tags=["SEO Technical"]
)


@router.post("/audit")
def audit_technical(request: AuditRequest):
    """
    Ejecuta una auditoría técnica SEO sin guardar información
    en una base de datos interna.

    El API Gateway administra el identificador y el historial
    general de la auditoría.
    """

    website = str(request.website)

    try:

        result = analyze_site(website)

        return {
            "success": True,
            "module": "seo-technical",
            "audit_id": request.audit_id,
            "status": "completed",
            "score": result.get("score", 0),
            "analysis": {
                "website": website,
                "keyword": request.keyword,
                "https": result.get("https", {}),
                "http_status": result.get("http_status", {}),
                "response_time": result.get("response_time", {}),
                "robots": result.get("robots", {}),
                "sitemap": result.get("sitemap", {}),
                "redirect": result.get("redirect", {}),
                "canonical": result.get("canonical", {}),
                "meta_robots": result.get("meta_robots", {})
            },
            "issues": result.get("issues", []),
            "recommendations": result.get(
                "recommendations",
                []
            ),
            "errors": []
        }

    except Exception as error:

        return {
            "success": False,
            "module": "seo-technical",
            "audit_id": request.audit_id,
            "status": "failed",
            "score": 0,
            "analysis": {
                "website": website,
                "keyword": request.keyword
            },
            "issues": [],
            "recommendations": [],
            "errors": [
                str(error)
            ]
        }
