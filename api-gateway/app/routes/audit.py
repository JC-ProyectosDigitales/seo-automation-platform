from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from shared.contracts import AuditRequest

from app.services.audit_service import create_audit

from app.database.session import get_db


router = APIRouter()


@router.post("/audit")
async def create(
    request: AuditRequest,
    db: Session = Depends(get_db)
):


    audit = await create_audit(
        request,
        db
    )


    return {

        "success": True,

        "module": "api-gateway",

        "audit_id": audit["audit_id"],

        "data": audit,

        "errors": []

    }