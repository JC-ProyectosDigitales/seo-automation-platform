from app.utils.audit_id import generate_audit_id

from app.database.models import Audit



async def create_audit(
    data,
    db
):


    audit_id = generate_audit_id()


    audit = {

        "audit_id": audit_id,

        "website": str(data.website),

        "keyword": data.keyword

    }



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



    return {

        "audit": audit,

        "audit_id": audit_id,

        "status": "pending"

    }