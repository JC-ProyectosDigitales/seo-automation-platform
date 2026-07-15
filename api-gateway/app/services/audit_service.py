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


    # Crear auditoría inicial
    db_audit = Audit(

        audit_id=audit_id,

        website=str(data.website),

        keyword=data.keyword,

        status="pending",

        results={}

    )


    db.add(db_audit)

    db.commit()

    db.refresh(db_audit)


    # Marcar auditoría como ejecutándose
    db_audit.status = "running"

    db.commit()


    try:

        # Ejecutar módulos SEO
        results = await run_audit(audit)


        # Guardar resultados finales
        db_audit.status = "completed"

        db_audit.results = results

        db.commit()

        db.refresh(db_audit)


    except Exception as error:

        db_audit.status = "failed"

        db_audit.results = {
            "error": str(error)
        }

        db.commit()

        db.refresh(db_audit)


        return {

            "audit_id": audit_id,

            "status": "failed",

            "modules": db_audit.results

        }


    return {

        "audit_id": audit_id,

        "status": db_audit.status,

        "modules": db_audit.results

    }
