from pydantic import BaseModel, HttpUrl
from typing import Optional


class AuditRequest(BaseModel):
    website: HttpUrl
    keyword: Optional[str] = None
    content: Optional[str] = None