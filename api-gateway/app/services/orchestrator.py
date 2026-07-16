from sqlalchemy.orm import Session

from app.services.module_client import send_request
from app.services.module_service import get_active_modules



async def run_audit(
    audit,
    db: Session
):

    results = {}


    modules = get_active_modules(
        db
    )


    for module in modules:


        response = await send_request(

            module["url"],

            audit,

            module["timeout"]

        )


        results[module["name"]] = {

            "priority": module["priority"],

            "timeout": module["timeout"],

            "result": response

        }


    return results