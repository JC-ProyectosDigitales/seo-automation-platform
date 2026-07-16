# Development Guide

## Descripción

Este documento explica el flujo de desarrollo de SEO Automation Platform.

Su objetivo es establecer una guía común para que todos los integrantes puedan desarrollar nuevos servicios, probar cambios e integrar sus APIs con el sistema principal.

---

# Requisitos del entorno

Antes de iniciar el desarrollo se necesita:

| Herramienta    | Uso                       |
|----------------|---------------------------|
| Docker         | Ejecución de contenedores |
| Docker Compose | Orquestación de servicios |
| Python 3.12    | Desarrollo backend        |
| Node.js        | Dashboard frontend        |
| Git            | Control de versiones      |

---

# Estructura del proyecto

seo-automation-platform/

├── api-gateway/
│
├── dashboard/
│
├── database/
│
├── services/
│ ├── ai-agent/
│ ├── seo-content/
│ ├── seo-monitor/
│ ├── seo-onpage/
│ └── seo-technical/
│
├── docs/
│
├── docker-compose.yml
└── README.md


---

# Ejecución del proyecto

## Levantar todos los servicios

Desde la raíz del proyecto:

docker compose up --build

Esto inicia:

API Gateway.
Base de datos.
Servicios SEO.
Dashboard.
Reiniciar un servicio específico

Ejemplo:

docker compose restart api-gateway
Ver logs

Ejemplo:

docker compose logs -f api-gateway
Desarrollo de un nuevo servicio

Cada servicio debe mantener una estructura similar:

nuevo-servicio/

├── Dockerfile
├── requirements.txt
│
└── app/
    ├── main.py
    │
    ├── routes/
    │   └── audit.py
    │
    └── services/
Creación del servicio

El servicio debe incluir:

main.py

Responsable de:

Crear la aplicación FastAPI.
Registrar rutas.
Configurar el servicio.

Ejemplo:

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health():

    return {
        "service": "nuevo-servicio",
        "status": "running"
    }
Endpoint de auditoría

Todos los servicios SEO deben implementar:

POST /audit

Este endpoint recibe información de una auditoría.

Ejemplo:

{
    "audit_id": "AUD-20260716-001",
    "website": "https://ejemplo.com",
    "keyword": "seo"
}
Respuesta estándar

Respuesta exitosa:

{
    "success": true,
    "service": "seo-content",
    "data": {},
    "error": null
}

Respuesta con error:

{
    "success": false,
    "service": "seo-content",
    "data": null,
    "error": "Mensaje del error"
}
Variables de entorno

Cada servicio debe manejar configuración mediante:

.env

Ejemplo:

SERVICE_NAME=seo-content

SERVICE_PORT=8000

API_GATEWAY_URL=http://api-gateway:5000

TIMEOUT=30
Registro de un módulo

Para integrar un nuevo servicio:

Crear el contenedor.
Exponer el endpoint /audit.
Registrar el módulo en API Gateway.

Ejemplo:

{
    "name": "seo-content",
    "url": "http://seo-content:8000",
    "priority": 1,
    "timeout": 30
}
Pruebas de API

Las APIs pueden probarse utilizando:

Swagger UI.
Postman.
Curl.

FastAPI genera documentación automática:

http://localhost:8000/docs
Reglas de desarrollo

Todos los integrantes deben:

Mantener separación por servicios.
No modificar servicios ajenos sin coordinación.
Utilizar JSON para comunicación.
Documentar nuevos endpoints.
Mantener nombres consistentes.
Crear commits descriptivos.
Flujo Git recomendado

Antes de realizar cambios:

git pull

Crear rama:

git checkout -b feature/nombre-servicio

Realizar cambios:

git add .
git commit -m "Descripción del cambio"

Enviar cambios:

git push origin feature/nombre-servicio
Checklist antes de integrar

Antes de entregar un servicio:

 Dockerfile funcional.
 requirements.txt actualizado.
 Endpoint /audit funcionando.
 Respuestas JSON correctas.
 Variables de entorno documentadas.
 Servicio probado localmente.
 Documentación actualizada.
Objetivo

Mantener una arquitectura organizada donde cada integrante pueda desarrollar su servicio de forma independiente y posteriormente integrarlo con la plataforma principal mediante el API Gateway.

