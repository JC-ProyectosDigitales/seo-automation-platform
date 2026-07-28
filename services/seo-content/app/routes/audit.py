from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl

from modules.audit_service import execute as execute_audit
from modules.web_scraper import extract_content


router = APIRouter(
    tags=["SEO Content"],
)


class AuditRequest(BaseModel):
    audit_id: str = Field(min_length=1)
    website: HttpUrl
    keyword: str = Field(min_length=1)
    content: str | None = None


@router.post("/audit")
def audit_content(data: AuditRequest):
    try:
        website = str(data.website)
        keyword = data.keyword.strip()

        page = extract_content(
            url=website,
            supplied_content=data.content,
        )

        result = execute_audit(
            audit_id=data.audit_id,
            website=website,
            keyword=keyword,
            page=page,
        )

        return result

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "module": "seo-content",
                "audit_id": data.audit_id,
                "status": "failed",
                "score": 0,
                "analysis": {},
                "issues": [],
                "recommendations": [],
                "errors": [
                    str(error),
                ],
            },
        )
