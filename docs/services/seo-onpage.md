# Servicio SEO OnPage

## Descripción

El servicio SEO OnPage es responsable de analizar elementos internos de una página web para identificar oportunidades de optimización relacionadas con estructura, contenido y configuración HTML.

Este servicio será consumido por el API Gateway durante una auditoría SEO.


---

# Responsabilidad del servicio

El servicio debe analizar:

- Títulos HTML.
- Meta descripción.
- Encabezados H1, H2 y H3.
- Uso de palabras clave.
- Etiquetas ALT en imágenes.
- Estructura básica del contenido.


---

# Arquitectura

Flujo de comunicación:
# Servicio SEO OnPage

## Descripción

El servicio SEO OnPage es responsable de analizar elementos internos de una página web para identificar oportunidades de optimización relacionadas con estructura, contenido y configuración HTML.

Este servicio será consumido por el API Gateway durante una auditoría SEO.


---

# Responsabilidad del servicio

El servicio debe analizar:

- Títulos HTML.
- Meta descripción.
- Encabezados H1, H2 y H3.
- Uso de palabras clave.
- Etiquetas ALT en imágenes.
- Estructura básica del contenido.


---

# Arquitectura

Flujo de comunicación:

Dashboard
|
v
API Gateway
|
v
seo-onpage
|
v
Resultado del análisis



El servicio no debe comunicarse directamente con el dashboard.

Toda comunicación debe pasar por el API Gateway.


---

# Endpoint requerido

## Ejecutar auditoría OnPage


Método:


POST



Ruta:


/audit



---

# Request


Ejemplo:

```json
{
    "audit_id": "AUD-20260716-001",
    "website": "https://ejemplo.com",
    "keyword": "seo"
}

Campos:

| Campo    | Tipo   | Descripción                |
| -------- | ------ | -------------------------- |
| audit_id | string | Identificador de auditoría |
| website  | string | URL del sitio a analizar   |
| keyword  | string | Palabra clave objetivo     |

Response

Ejemplo:

{
    "success": true,
    "module": "seo-onpage",
    "audit_id": "AUD-20260716-001",
    "score": 85,
    "issues": [
        {
            "type": "warning",
            "message": "Meta description demasiado corta"
        }
    ],
    "recommendations": [
        "Agregar etiquetas ALT en imágenes",
        "Mejorar estructura de encabezados"
    ]
}
Estados posibles
Auditoría completada
{
    "status": "completed"
}
Error
{
    "status": "error",
    "message": "Descripción del error"
}
Integración con API Gateway

El API Gateway enviará:

URL del sitio.
Keyword.
Identificador de auditoría.

El servicio debe responder:

Resultado del análisis.
Problemas encontrados.
Recomendaciones.
Restricciones

El servicio debe:

Mantener comunicación mediante REST API.
Utilizar JSON como formato de intercambio.
No modificar la base de datos directamente.
No depender del dashboard.
Respetar el contrato definido en api-contract.md.