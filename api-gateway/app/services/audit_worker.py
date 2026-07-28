from datetime import datetime
from typing import List, Optional

from app.database.models import Audit
from app.services.orchestrator import run_audit


async def execute_audit(
    audit: dict,
    db,
    selected_modules: Optional[List[str]] = None,
):
    audit_id = audit["audit_id"]

    db_audit = (
        db.query(Audit)
        .filter(
            Audit.audit_id == audit_id
        )
        .first()
    )

    if not db_audit:
        return

    try:
        start_time = datetime.utcnow()

        db_audit.status = "running"
        db_audit.started_at = start_time
        db_audit.error_message = None

        db.commit()
        db.refresh(db_audit)

        results = await run_audit(
            audit=audit,
            db=db,
            selected_modules=selected_modules,
        )

        end_time = datetime.utcnow()

        execution_time = (
            end_time - start_time
        ).total_seconds()

        db_audit.status = "completed"
        db_audit.results = results
        db_audit.completed_at = end_time
        db_audit.execution_time = execution_time

        db.commit()
        db.refresh(db_audit)

    except Exception as error:
        end_time = datetime.utcnow()

        db_audit.status = "failed"
        db_audit.completed_at = end_time
        db_audit.error_message = str(error)

        if db_audit.started_at:
            db_audit.execution_time = (
                end_time - db_audit.started_at
            ).total_seconds()

        db.commit()
