from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from sqlalchemy import func

from app.database.session import get_db
from app.database.models import Audit, Module


router = APIRouter()



@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db)
):


    total_audits = (
        db.query(Audit)
        .count()
    )


    completed_audits = (
        db.query(Audit)
        .filter(
            Audit.status == "completed"
        )
        .count()
    )


    pending_audits = (
        db.query(Audit)
        .filter(
            Audit.status == "pending"
        )
        .count()
    )


    active_modules = (
        db.query(Module)
        .filter(
            Module.active == True
        )
        .count()
    )


    return {

        "success": True,

        "stats": {

            "total_audits": total_audits,

            "completed_audits": completed_audits,

            "pending_audits": pending_audits,

            "active_modules": active_modules

        }

    }