from fastapi import APIRouter, BackgroundTasks, Depends

from sqlalchemy.orm import Session

from shared.contracts import AuditRequest

from app.database.session import get_db
from app.services.audit_service import create_audit
from app.services.audit_worker import execute_audit


router = APIRouter()


@router.post("/audit")
async def create(
    request: AuditRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    audit = await create_audit(
        request,
        db,
    )

    selected_modules = request.modules

    background_tasks.add_task(
        execute_audit,
        audit["audit"],
        db,
        selected_modules,
    )

    return {
        "success": True,
        "module": "api-gateway",
        "audit_id": audit["audit_id"],
        "data": {
            "audit_id": audit["audit_id"],
            "status": audit["status"],
            "requested_modules": selected_modules or "all",
        },
        "errors": [],
    }
