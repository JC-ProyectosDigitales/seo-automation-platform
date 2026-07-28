from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.models import Module


def get_active_modules(
    db: Session,
    selected_modules: Optional[List[str]] = None,
):
    query = (
        db.query(Module)
        .filter(
            Module.active.is_(True)
        )
    )

    if selected_modules:
        normalized_names = {
            module_name.strip().lower()
            for module_name in selected_modules
            if module_name and module_name.strip()
        }

        query = query.filter(
            Module.name.in_(normalized_names)
        )

    modules = (
        query
        .order_by(
            Module.priority.asc()
        )
        .all()
    )

    result = []

    for module in modules:
        result.append(
            {
                "id": module.id,
                "name": module.name,
                "url": module.url,
                "description": module.description,
                "priority": module.priority,
                "timeout": module.timeout,
            }
        )

    return result
