from fastapi import APIRouter

from app.models.audit_request import AuditRequest
from app.modules.analyzer import analyze_page


router = APIRouter()


@router.post("/audit")
async def audit_onpage(
    request: AuditRequest,
):
    result = await analyze_page(
        website=str(request.website),
        keyword=request.keyword,
    )

    return {
        "success": result["success"],
        "module": "seo-onpage",
        "audit_id": request.audit_id,
        "status": (
            "completed"
            if result["success"]
            else "failed"
        ),
        "score": result["score"],
        "analysis": result["analysis"],
        "issues": result["issues"],
        "recommendations": result["recommendations"],
        "errors": result["errors"],
    }
