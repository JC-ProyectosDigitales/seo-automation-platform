import os

from app.utils.audit_id import generate_audit_id
from app.services.orchestrator import run_audit

from app.database.models import Audit


async def create_audit(data, db):

    audit_id = generate_audit_id()


    audit = {

        "audit_id": audit_id,

        "website": str(data.website),

        "keyword": data.keyword

    }


    results = await run_audit(audit)



    db_audit = Audit(

        audit_id=audit_id,

        website=str(data.website),

        keyword=data.keyword,

        status="completed",

        results=results

    )


    db.add(db_audit)

    db.commit()

    db.refresh(db_audit)



    return {

        "audit_id": audit_id,

        "status": "completed",

        "modules": results

    }