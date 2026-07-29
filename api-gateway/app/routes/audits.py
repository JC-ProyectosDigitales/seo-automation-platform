from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Audit
from app.database.session import get_db


router = APIRouter()


@router.get("/audits")
def get_audits(
    db: Session = Depends(get_db)
):
    audits = (
        db.query(Audit)
        .order_by(
            Audit.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "total": len(audits),
        "audits": [
            {
                "audit_id": audit.audit_id,
                "website": audit.website,
                "keyword": audit.keyword,
                "status": audit.status,
                "created_at": audit.created_at
            }
            for audit in audits
        ]
    }


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )

    return {
        "success": True,
        "audit_id": audit.audit_id,
        "website": audit.website,
        "keyword": audit.keyword,
        "status": audit.status,
        "results": audit.results,
        "created_at": audit.created_at
    }


@router.delete("/audits/{audit_id}")
def delete_audit(
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )

    db.delete(audit)
    db.commit()

    return {
        "success": True,
        "message": "Audit deleted successfully",
        "audit_id": audit_id
    }
