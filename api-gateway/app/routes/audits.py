from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Audit


router = APIRouter()


@router.get("/audits/{audit_id}")
def get_audit(
    audit_id: str,
    db: Session = Depends(get_db)
):

    audit = (
        db.query(Audit)
        .filter(
            Audit.audit_id == audit_id
        )
        .first()
    )


    if not audit:

        return {
            "success": False,
            "error": "Audit not found"
        }


    return {
        "audit_id": audit.audit_id,
        "website": audit.website,
        "keyword": audit.keyword,
        "status": audit.status,
        "results": audit.results,
        "created_at": audit.created_at
    }