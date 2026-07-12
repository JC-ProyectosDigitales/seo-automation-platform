from pydantic import BaseModel


class AuditRequest(BaseModel):

    website: str

    keyword: str