from sqlalchemy.orm import Session

from app.database.models import Module



def get_active_modules(
    db: Session
):

    modules = (
        db.query(Module)
        .filter(
            Module.active == True
        )
        .order_by(
            Module.priority.asc()
        )
        .all()
    )


    result = []


    for module in modules:

        result.append({

            "id": module.id,

            "name": module.name,

            "url": module.url,

            "description": module.description,

            "priority": module.priority,

            "timeout": module.timeout

        })


    return result