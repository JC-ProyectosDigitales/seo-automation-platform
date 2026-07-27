from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from modules.audit_service import execute as execute_audit
from modules.web_scraper import extract_content


router = APIRouter()


class AuditRequest(BaseModel):
    audit_id: str
    website: str
    keyword: str


@router.post("/audit")
def audit_content(data: AuditRequest):

    try:

        content = extract_content(data.website)

        result = execute_audit(
            data.audit_id,
            data.keyword,
            content
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
                "errors": [
                    str(error)
                ]
            }
        )