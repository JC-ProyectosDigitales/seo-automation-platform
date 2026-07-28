from fastapi import APIRouter

from app.models.audit_request import AuditRequest
from app.modules.analyzer import analyze_monitoring


router = APIRouter()


@router.post("/audit")
async def audit_monitor(
    request: AuditRequest,
):
    result = await analyze_monitoring(
        website=str(request.website),
    )

    return {
        "success": result["success"],
        "module": "seo-monitor",
        "audit_id": request.audit_id,
        "status": (
            "completed"
            if result["success"]
            else "failed"
        ),
        "score": result["score"],
        "analysis": result["analysis"],
        "issues": result["issues"],
        "recommendations": (
            result["recommendations"]
        ),
        "errors": result["errors"],
    }
