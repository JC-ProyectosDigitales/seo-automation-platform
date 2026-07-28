from pydantic import BaseModel, Field, HttpUrl


class AuditRequest(BaseModel):
    """
    Datos necesarios para ejecutar una auditoría técnica SEO.

    El audit_id es generado y enviado por el API Gateway.
    """

    audit_id: str = Field(
        ...,
        min_length=1,
        description="Identificador de la auditoría generado por el Gateway."
    )

    website: HttpUrl = Field(
        ...,
        description="URL del sitio que será analizado."
    )

    keyword: str | None = Field(
        default=None,
        description="Palabra clave asociada a la auditoría."
    )
