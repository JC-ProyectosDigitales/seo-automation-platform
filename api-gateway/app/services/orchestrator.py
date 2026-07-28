from typing import List, Optional

from sqlalchemy.orm import Session

from app.services.module_client import send_request
from app.services.module_service import get_active_modules


async def run_audit(
    audit: dict,
    db: Session,
    selected_modules: Optional[List[str]] = None,
):
    results = {}

    requested_modules = {
        module_name.strip().lower()
        for module_name in selected_modules or []
        if module_name and module_name.strip()
    }

    modules = get_active_modules(
        db=db,
        selected_modules=list(requested_modules) if requested_modules else None,
    )

    found_modules = {
        module["name"].lower()
        for module in modules
    }

    missing_modules = requested_modules - found_modules

    for missing_module in sorted(missing_modules):
        results[missing_module] = {
            "priority": None,
            "timeout": None,
            "result": {
                "success": False,
                "module": missing_module,
                "audit_id": audit.get("audit_id"),
                "status": "failed",
                "score": None,
                "analysis": {},
                "issues": [],
                "recommendations": [],
                "errors": [
                    {
                        "code": "MODULE_NOT_AVAILABLE",
                        "message": (
                            "El módulo solicitado no existe, "
                            "no está activo o no está disponible."
                        ),
                    }
                ],
            },
        }

    for module in modules:
        response = await send_request(
            module["url"],
            audit,
            module["timeout"],
        )

        results[module["name"]] = {
            "priority": module["priority"],
            "timeout": module["timeout"],
            "result": response,
        }

    return results
