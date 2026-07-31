from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse


from app.database.models import Audit
from app.database.session import get_db

from app.services.pdf_report_service import (
    build_audit_pdf,
)

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

@router.get("/audits/{audit_id}/report")
def download_audit_report(
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

    if audit.status in {
        "pending",
        "running",
        "processing",
    }:
        raise HTTPException(
            status_code=(
                status.HTTP_409_CONFLICT
            ),
            detail=(
                "La auditoría todavía está "
                "en proceso."
            )
        )

    try:
        pdf_buffer = build_audit_pdf(
            audit
        )

    except Exception as error:
        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "No fue posible generar "
                "el reporte PDF."
            )
        ) from error

    filename = (
        f"reporte-{audit.audit_id}.pdf"
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
            "Cache-Control": "no-store",
        }
    )

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
