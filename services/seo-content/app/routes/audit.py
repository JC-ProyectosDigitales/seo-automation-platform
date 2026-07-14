from fastapi import APIRouter


router = APIRouter()


@router.post("/audit")
async def audit_content(data: dict):

    return {

        "success": True,

        "module": "seo-content",

        "audit_id": data.get("audit_id"),

        "data": {

            "message": "SEO Content service received audit",

            "keyword": data.get("keyword"),

            "website": data.get("website")

        },

        "errors": []

    }