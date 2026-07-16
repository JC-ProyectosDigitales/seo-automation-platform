# Servicio SEO Technical

## Descripción

El servicio SEO Technical es responsable de analizar aspectos técnicos de un sitio web que pueden afectar su indexación, rastreo y rendimiento en motores de búsqueda.

Este servicio será ejecutado como parte del proceso de auditoría SEO mediante el API Gateway.


---

# Responsabilidad del servicio

El servicio debe analizar:

- Archivo robots.txt.
- Archivo sitemap.xml.
- Código de respuesta HTTP.
- Tiempo de carga básico.
- Seguridad HTTPS.
- Etiquetas técnicas SEO.
- Configuración básica para rastreo.


---

# Arquitectura

Flujo de comunicación:

Dashboard
|
v
API Gateway
|
v
seo-technical
|
v
Resultado del análisis



El servicio no debe comunicarse directamente con el dashboard.

Toda solicitud debe pasar por el API Gateway.


---

# Endpoint requerido

## Ejecutar auditoría técnica


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

| Campo    | Tipo   | Descripción                      |
| -------- | ------ | -------------------------------- |
| audit_id | string | Identificador único de auditoría |
| website  | string | URL del sitio a analizar         |
| keyword  | string | Palabra clave relacionada        |

Response

Ejemplo:

{
    "success": true,
    "module": "seo-technical",
    "audit_id": "AUD-20260716-001",
    "score": 90,
    "analysis": {
        "https": true,
        "robots_txt": true,
        "sitemap": true,
        "response_time": 350
    },
    "issues": [
        {
            "type": "warning",
            "message": "Tiempo de respuesta elevado"
        }
    ],
    "recommendations": [
        "Optimizar recursos del servidor",
        "Revisar configuración del sitemap"
    ]
}
Datos esperados del análisis
HTTPS

Debe verificar:

Uso de certificado SSL.
Disponibilidad mediante HTTPS.
Robots.txt

Debe comprobar:

Existencia del archivo.
Permisos de rastreo.
Sitemap

Debe comprobar:

Existencia de sitemap.xml.
Accesibilidad del archivo.
Rendimiento

Puede evaluar:

Tiempo de respuesta.
Disponibilidad del sitio.
Errores HTTP.
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

Audit ID.
URL del sitio.
Información necesaria para análisis.

El servicio responderá:

Estado técnico del sitio.
Problemas encontrados.
Recomendaciones.
Restricciones

El servicio debe:

Comunicarse mediante REST API.
Utilizar JSON.
No modificar la base de datos directamente.
No depender del dashboard.
Mantener compatibilidad con el contrato definido en api-contract.md.