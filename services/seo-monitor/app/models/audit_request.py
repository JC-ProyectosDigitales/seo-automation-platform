from typing import Optional

from pydantic import BaseModel, HttpUrl


class AuditRequest(BaseModel):
    audit_id: str
    website: HttpUrl
    keyword: Optional[str] = None
    content: Optional[str] = None
