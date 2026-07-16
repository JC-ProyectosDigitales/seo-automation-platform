# Servicio SEO Monitor

## Descripción

El servicio SEO Monitor es responsable de realizar seguimiento de métricas SEO a través del tiempo y almacenar información relacionada con la evolución de una auditoría.

Su objetivo es permitir comparar resultados históricos, identificar cambios y generar información útil para el seguimiento del rendimiento SEO.

Este servicio será utilizado por el API Gateway y el dashboard.


---

# Responsabilidad del servicio

El servicio debe gestionar:

- Historial de auditorías.
- Evolución de puntuaciones SEO.
- Comparación entre auditorías.
- Registro de cambios.
- Métricas generales del sistema.


---

# Arquitectura

Flujo de comunicación:

Dashboard
|
v
API Gateway
|
v
seo-monitor
|
v
Métricas e historial



El servicio no debe comunicarse directamente con el dashboard.

Todas las solicitudes deben pasar por el API Gateway.


---

# Funciones principales


## Registro de métricas

Debe permitir guardar información generada por otros módulos SEO.

Ejemplo:

- Score general.
- Score por módulo.
- Fecha de ejecución.
- Estado de auditoría.


---

## Consulta histórica

Debe permitir obtener:

- Auditorías realizadas.
- Resultados anteriores.
- Evolución del rendimiento.


---

## Comparación de auditorías

Debe permitir comparar:

- Auditoría actual.
- Auditoría anterior.
- Cambios detectados.


Ejemplo:

```json
{
    "previous_score": 70,
    "current_score": 85,
    "improvement": 15
}
Endpoints requeridos
Registrar métrica

Método:

POST

Ruta:

/metrics

Request:

{
    "audit_id": "AUD-20260716-001",
    "score": 85,
    "modules": {
        "seo-content": 80,
        "seo-onpage": 90,
        "seo-technical": 85
    }
}

Response:

{
    "success": true,
    "message": "Metric stored"
}
Obtener historial

Método:

GET

Ruta:

/history/{website}

Response:

{
    "success": true,
    "website": "https://ejemplo.com",
    "history": [
        {
            "date": "2026-07-16",
            "score": 85
        }
    ]
}
Comparar auditorías

Método:

GET

Ruta:

/compare/{audit_id_1}/{audit_id_2}

Response:

{
    "success": true,
    "comparison": {
        "score_difference": 10,
        "improvements": [
            "Mejor estructura HTML",
            "Mayor optimización de contenido"
        ]
    }
}
Datos gestionados
Métricas generales

Ejemplo:

Campo	Tipo
audit_id	string
website	string
score	integer
created_at	datetime
Métricas por módulo

Ejemplo:

{
    "seo-content": 80,
    "seo-onpage": 90,
    "seo-technical": 85
}
Integración con API Gateway

El API Gateway será responsable de:

Solicitar métricas.
Consultar historial.
Exponer información al dashboard.

El servicio responderá:

Datos históricos.
Comparaciones.
Estadísticas.
Restricciones

El servicio debe:

Utilizar REST API.
Trabajar con JSON.
Mantener separación de responsabilidades.
No depender del dashboard.
No ejecutar auditorías directamente.
No modificar módulos externos.