# Servicio AI Agent

## Descripción

El servicio AI Agent es responsable de procesar información generada por los módulos SEO y utilizar modelos de inteligencia artificial para generar recomendaciones, análisis y sugerencias de optimización.

Su función principal es actuar como una capa inteligente entre los resultados técnicos obtenidos y las recomendaciones finales mostradas al usuario.

---

# Responsabilidad del servicio

El servicio debe encargarse de:

- Interpretar resultados de auditorías SEO.
- Generar recomendaciones automáticas.
- Priorizar problemas encontrados.
- Crear resúmenes de auditoría.
- Explicar posibles mejoras.

---

# Arquitectura

Flujo de comunicación:

Dashboard
|
v
API Gateway
|
v
AI Agent
|
v
Modelo de IA
|
v
Recomendaciones SEO


El servicio no debe comunicarse directamente con el dashboard.

Todas las solicitudes deben pasar por el API Gateway.

---

# Funciones principales

## Análisis de resultados

El servicio recibe resultados generados por:

- seo-content.
- seo-onpage.
- seo-technical.
- seo-monitor.

Ejemplo:

```json
{
    "audit_id": "AUD-20260716-001",
    "results": {
        "seo-content": {
            "score": 80
        },
        "seo-technical": {
            "score": 90
        }
    }
}
Generación de recomendaciones

El servicio debe generar recomendaciones basadas en:

Problemas detectados.
Prioridad.
Impacto SEO.
Buenas prácticas.

Ejemplo:

{
    "recommendations": [
        {
            "priority": "high",
            "message": "Optimizar etiquetas title"
        },
        {
            "priority": "medium",
            "message": "Mejorar descripción meta"
        }
    ]
}
Resumen automático

Debe generar una explicación general del estado SEO.

Ejemplo:

{
    "summary": "El sitio presenta buena configuración técnica pero requiere mejoras en contenido."
}
Endpoint requerido
Generar análisis inteligente

Método:

POST

Ruta:

/analyze
Request

Ejemplo:

{
    "audit_id": "AUD-20260716-001",
    "results": {
        "seo-content": {},
        "seo-onpage": {},
        "seo-technical": {}
    }
}

Campos:

| Campo    | Tipo   | Descripción                      |
| -------- | ------ | -------------------------------- |
| audit_id | string | Identificador de auditoría       |
| results  | object | Resultados obtenidos por módulos |

Response

Ejemplo:

{
    "success": true,
    "audit_id": "AUD-20260716-001",
    "analysis": {
        "summary": "El sitio necesita mejoras de contenido.",
        "recommendations": [
            {
                "priority": "high",
                "message": "Agregar etiquetas ALT a imágenes"
            }
        ]
    }
}
Integración con API Gateway

El API Gateway será responsable de:

Enviar resultados de auditorías.
Solicitar análisis inteligente.
Entregar recomendaciones al dashboard.

El AI Agent responderá:

Resumen SEO.
Recomendaciones.
Prioridades.
Restricciones

El servicio debe:

Comunicarse mediante REST API.
Utilizar JSON.
No ejecutar análisis SEO directamente.
No acceder directamente a la base de datos principal.
Mantener independencia del modelo de IA utilizado.
Permitir reemplazar el proveedor de IA.
Consideraciones futuras

El servicio puede extenderse para:

Integración con diferentes modelos LLM.
Generación de contenido optimizado.
Explicaciones personalizadas.
Chat SEO asistido.

Estas funciones no forman parte del alcance inicial.
