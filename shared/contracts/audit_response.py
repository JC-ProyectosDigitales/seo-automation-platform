from pydantic import BaseModel
from typing import Any, Dict


class AuditResponse(BaseModel):

    success: bool

    audit_id: str

    website: str

    status: str

    results: Dict[str, Any] = {}