# API Gateway

## Descripción

El API Gateway es el punto central de comunicación de la plataforma SEO Automation Platform.

Su función es recibir las solicitudes del dashboard, administrar las auditorías, comunicarse con los microservicios SEO y devolver respuestas unificadas al cliente.

El API Gateway funciona como intermediario entre:

- Dashboard Web.
- Servicios SEO.
- Base de datos.
- Servicios inteligentes.

---

# Arquitectura de comunicación

Flujo general:

Usuario
|
v
Dashboard Web
|
v
API Gateway
|
+----------------+
| |
v v
SEO Services AI Agent

|
v

Database


---

# Responsabilidades

El API Gateway debe encargarse de:

- Recibir solicitudes del frontend.
- Validar información enviada.
- Crear auditorías.
- Administrar estados de ejecución.
- Coordinar la ejecución de módulos.
- Guardar resultados.
- Exponer información al dashboard.

---

# Tecnologías

Implementación actual:

| Tecnología | Uso                    |
|------------|------------------------|
| FastAPI    | Framework backend      |
| SQLAlchemy | ORM para base de datos |
| PostgreSQL | Persistencia           |
| Docker     | Contenedores           |

---

# Estructura actual


api-gateway/

app/
├── main.py
│
├── routes/
│ ├── audits.py
│ ├── modules.py
│ ├── stats.py
│
├── database/
│ ├── models.py
│ ├── connection.py
│ └── session.py
│
└── services/


---

# Endpoints principales

## Auditorías

---

## Crear auditoría

Método:


POST


Ruta:


/audits


Descripción:

Crea una nueva auditoría SEO.

Request:

```json
{
    "website": "https://ejemplo.com",
    "keyword": "seo"
}

Response:

{
    "success": true,
    "audit_id": "AUD-20260716-001",
    "status": "pending"
}
Obtener auditoría

Método:

GET

Ruta:

/audits/{audit_id}

Descripción:

Obtiene información detallada de una auditoría.

Response:

{
    "audit_id": "AUD-20260716-001",
    "website": "https://ejemplo.com",
    "keyword": "seo",
    "status": "completed",
    "results": {}
}
Obtener historial

Método:

GET

Ruta:

/audits

Descripción:

Obtiene todas las auditorías realizadas.

Response:

{
    "success": true,
    "total": 20,
    "audits": []
}
Módulos SEO

Los módulos representan servicios externos que ejecutan análisis específicos.

Obtener módulos registrados

Método:

GET

Ruta:

/modules

Response:

{
    "success": true,
    "modules": [
        {
            "name": "seo-content",
            "active": true,
            "priority": 1
        }
    ]
}
Registrar módulo

Método:

POST

Ruta:

/modules

Request:

{
    "name": "seo-content",
    "url": "http://seo-content:8000",
    "priority": 1,
    "timeout": 30
}
Estadísticas
Obtener métricas generales

Método:

GET

Ruta:

/stats

Response:

{
    "success": true,
    "stats": {
        "total_audits": 20,
        "completed_audits": 19,
        "pending_audits": 1,
        "active_modules": 3
    }
}
Comunicación con servicios SEO

Cada servicio debe exponer una API REST independiente.

Ejemplo:

API Gateway
      |
      |
      v

seo-content:8000
seo-onpage:8000
seo-technical:8000
seo-monitor:8000
ai-agent:8000
Contrato de respuesta de servicios

Todos los servicios deben responder utilizando una estructura estándar:

{
    "success": true,
    "service": "seo-content",
    "data": {},
    "error": null
}
Manejo de errores

Cuando ocurre un error:

{
    "success": false,
    "service": "seo-content",
    "data": null,
    "error": "Descripción del error"
}
Estados de auditoría

Las auditorías utilizan los siguientes estados:

| Estado    | Descripción                          |
| --------- | ------------------------------------ |
| pending   | Auditoría creada esperando ejecución |
| running   | Auditoría en proceso                 |
| completed | Auditoría finalizada correctamente   |
| failed    | Error durante ejecución              |

Reglas para nuevos servicios

Todo nuevo servicio integrado debe:

Tener API REST propia.
Utilizar JSON.
Registrar su módulo en el Gateway.
Respetar timeout configurado.
Mantener independencia del resto de servicios.
No acceder directamente al dashboard.
Objetivo del API Gateway

Centralizar la comunicación de la plataforma y permitir que los servicios SEO puedan desarrollarse de manera independiente por diferentes integrantes del equipo.
