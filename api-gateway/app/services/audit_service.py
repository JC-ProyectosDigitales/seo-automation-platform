import os

from app.utils.audit_id import generate_audit_id
from app.services.module_client import send_request
from app.services.modules import MODULES

from app.database.models import Audit


async def create_audit(data, db):

    audit_id = generate_audit_id()


    audit = {

        "audit_id": audit_id,

        "website": str(data.website),

        "keyword": data.keyword

    }


    results = {}


    for module, url in MODULES.items():

        response = await send_request(
            url,
            audit
        )

        results[module] = response



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