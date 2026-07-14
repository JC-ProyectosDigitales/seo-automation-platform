from pydantic import BaseModel
from typing import Any, List
from pydantic import Field


class ModuleResponse(BaseModel):
    success: bool

    module: str

    audit_id: str

    data: Any = {}

    errors: List[str] = Field(default_factory=list)