from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from modules.audit_service import execute as execute_audit
from modules.web_scraper import extract_content


router = APIRouter(
    tags=["SEO Content"]
)


class AuditRequest(BaseModel):
    audit_id: str = Field(min_length=1)
    website: str = Field(min_length=1)
    keyword: str = Field(min_length=1)


@router.post("/audit")
def audit_content(data: AuditRequest):
    try:
        content = extract_content(data.website)

        result = execute_audit(
            audit_id=data.audit_id,
            keyword=data.keyword,
            content=content
        )

        return result

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "module": "seo-content",
                "audit_id": data.audit_id,
                "status": "error",
                "score": 0,
                "analysis": {},
                "issues": [],
                "recommendations": [],
                "errors": [
                    str(error)
                ]
            }
        )
