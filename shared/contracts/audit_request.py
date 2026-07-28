from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class AuditRequest(BaseModel):
    website: HttpUrl
    keyword: Optional[str] = None
    content: Optional[str] = None

    modules: Optional[List[str]] = Field(
        default=None,
        description=(
            "Lista de módulos que deben ejecutarse. "
            "Si no se envía, se ejecutan todos los módulos activos."
        ),
    )
