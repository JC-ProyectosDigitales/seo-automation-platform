from fastapi import APIRouter

from app.schemas.audit_schema import AuditRequest

from app.services.audit_service import create_audit


router = APIRouter()


@router.post("/audit")
async def create(request: AuditRequest):


    audit = create_audit(request)


    return {

        "success":True,

        "module":"api-gateway",

        "audit_id":audit["audit_id"],

        "data":audit,

        "errors":[]

    }