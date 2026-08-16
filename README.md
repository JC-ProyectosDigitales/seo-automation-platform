# SEO Automation Platform

Plataforma web modular para ejecutar auditorías SEO sobre sitios reales mediante una arquitectura basada en microservicios.

SEO Automation Platform centraliza diferentes áreas de análisis —contenido, SEO On-Page, SEO técnico y monitoreo— mediante un API Gateway desarrollado con FastAPI, un Dashboard en React y persistencia en PostgreSQL.

El objetivo del proyecto es mantener cada área de análisis como un servicio independiente, permitiendo ampliar la plataforma sin concentrar toda la lógica SEO en una sola aplicación.

---

## Características principales

- Auditorías SEO sobre sitios web reales.
- Arquitectura basada en microservicios.
- Dashboard web con React y Vite.
- API Gateway desarrollado con FastAPI.
- Persistencia de auditorías en PostgreSQL.
- Historial y consulta individual de auditorías.
- Ejecución de todos los módulos o selección de módulos específicos.
- Registro y administración dinámica de módulos.
- Prioridad configurable por servicio.
- Timeout independiente por módulo.
- Manejo de errores entre servicios.
- Comunicación interna mediante APIs REST y JSON.
- Contenedores Docker independientes.
- Despliegue mediante Docker Compose y Nginx.

---

## Arquitectura

```text
                         Usuario
                            |
                            v
                    +---------------+
                    |   Dashboard   |
                    | React + Vite  |
                    |    Nginx      |
                    +-------+-------+
                            |
                            | /api
                            v
                    +---------------+
                    |  API Gateway  |
                    |    FastAPI    |
                    +-------+-------+
                            |
              +-------------+-------------+-------------+
              |             |             |             |
              v             v             v             v
      +-------------+ +-------------+ +-------------+ +-------------+
      | SEO Content | | SEO OnPage  | |SEO Technical| | SEO Monitor |
      |   :5003     | |   :5004     | |   :5005     | |   :5006     |
      +-------------+ +-------------+ +-------------+ +-------------+
              \             |             |             /
               \            |             |            /
                +-----------+-------------+-----------+
                            |
                            v
                      PostgreSQL
```

El API Gateway coordina la ejecución de los microservicios y almacena el resultado consolidado de cada auditoría.

---

## Flujo de una auditoría

```text
Usuario
  |
  v
Dashboard
  |
  v
POST /api/audit
  |
  v
API Gateway
  |
  +--> Registra la auditoría
  |
  +--> Obtiene módulos activos
  |
  +--> Filtra módulos seleccionados
  |
  +--> Ejecuta servicios por prioridad
  |
  v
Resultados consolidados
  |
  v
PostgreSQL
  |
  v
Dashboard
```

El Gateway también identifica módulos solicitados que no existen, están desactivados o no están disponibles y devuelve un error controlado para esos casos.

---

# Microservicios

## SEO Content

Servicio especializado en análisis y optimización de contenido.

Actualmente procesa:

- contenido obtenido desde una URL;
- palabra clave objetivo;
- estructura de encabezados;
- densidad de keywords;
- legibilidad;
- metadatos;
- puntuación SEO;
- problemas detectados;
- recomendaciones de optimización.

Endpoint interno:

```text
http://seo-content:5003/audit
```

Puerto publicado:

```text
5103
```

Prioridad predeterminada:

```text
10
```

---

## SEO OnPage

Servicio especializado en elementos SEO presentes dentro de una página.

La implementación actual utiliza un analizador propio y devuelve:

- puntuación;
- análisis;
- problemas;
- recomendaciones;
- errores.

Su dominio incluye elementos como:

- metadatos;
- títulos;
- encabezados;
- imágenes;
- atributos ALT;
- enlaces;
- elementos de optimización On-Page.

Endpoint interno:

```text
http://seo-onpage:5004/audit
```

Puerto publicado:

```text
5104
```

Prioridad predeterminada:

```text
20
```

---

## SEO Technical

Servicio especializado en aspectos técnicos que pueden afectar rastreo, indexación y funcionamiento SEO.

Actualmente analiza:

- HTTPS;
- estado HTTP;
- tiempo de respuesta;
- robots.txt;
- sitemap.xml;
- redirecciones;
- canonical;
- meta robots.

La respuesta incluye:

- score;
- análisis técnico;
- issues;
- recomendaciones;
- errores.

Endpoint interno:

```text
http://seo-technical:5005/audit
```

Puerto publicado:

```text
5105
```

Prioridad predeterminada:

```text
30
```

---

## SEO Monitor

Servicio encargado de analizar disponibilidad y estado operativo del sitio.

Actualmente evalúa:

- disponibilidad;
- tiempo de respuesta;
- redirecciones;
- código HTTP;
- content type;
- content length;
- servidor;
- certificado SSL.

A partir de estas métricas genera:

- puntuación;
- problemas detectados;
- recomendaciones;
- errores de monitoreo.

Endpoint interno:

```text
http://seo-monitor:5006/audit
```

Puerto publicado:

```text
5106
```

Prioridad predeterminada:

```text
40
```

---

# API Gateway

El API Gateway funciona como núcleo de coordinación de la plataforma.

Está desarrollado con:

- Python;
- FastAPI;
- SQLAlchemy;
- HTTPX;
- Pydantic;
- PostgreSQL.

Sus principales responsabilidades son:

- recibir solicitudes del Dashboard;
- crear auditorías;
- registrar información en PostgreSQL;
- obtener módulos activos;
- filtrar módulos seleccionados;
- ejecutar microservicios;
- aplicar prioridades;
- aplicar timeouts;
- detectar módulos no disponibles;
- consolidar resultados;
- mantener historial;
- administrar módulos;
- exponer estadísticas.

Puerto interno:

```text
5000
```

Puerto publicado:

```text
5100
```

---

## Módulos predeterminados

| Módulo | Prioridad | Timeout |
|---|---:|---:|
| `seo-content` | 10 | 30 s |
| `seo-onpage` | 20 | 30 s |
| `seo-technical` | 30 | 30 s |
| `seo-monitor` | 40 | 30 s |

Los módulos se registran automáticamente al iniciar el API Gateway si todavía no existen en PostgreSQL.

---

## Selección de módulos

El orquestador puede ejecutar todos los módulos activos o únicamente una selección solicitada.

Los módulos solicitados que no estén registrados, activos o disponibles generan una respuesta controlada:

```json
{
  "success": false,
  "status": "failed",
  "errors": [
    {
      "code": "MODULE_NOT_AVAILABLE",
      "message": "El módulo solicitado no existe, no está activo o no está disponible."
    }
  ]
}
```

---

# Dashboard

El frontend está desarrollado con:

- React;
- React Router;
- Vite;
- Axios.

El Dashboard se distribuye mediante Nginx dentro de Docker.

Puerto publicado:

```text
5173
```

Acceso local:

```text
http://localhost:5173
```

Nginx redirige las solicitudes:

```text
/api/
```

hacia:

```text
api-gateway:5000
```

Esto evita acoplar el frontend directamente a una dirección fija del backend.

---

# Base de datos

La plataforma utiliza PostgreSQL para almacenar principalmente:

## Auditorías

- identificador;
- sitio web;
- keyword;
- estado;
- resultados;
- errores;
- fechas de ejecución;
- tiempo de procesamiento.

## Módulos

- nombre;
- URL;
- descripción;
- estado activo;
- prioridad;
- timeout.

Los resultados de los servicios pueden almacenarse como estructuras JSON, permitiendo que cada microservicio entregue métricas diferentes.

---

# Tecnologías utilizadas

### Frontend

- React
- React Router
- Vite
- Axios
- Nginx

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- HTTPX
- Uvicorn

### Base de datos

- PostgreSQL

### Infraestructura

- Docker
- Docker Compose
- REST APIs
- JSON

### Testing

- pytest

---

# Estructura del proyecto

```text
seo-automation-platform/
├── api-gateway/
│   ├── app/
│   │   ├── database/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── Dockerfile
│   └── requirements.txt
│
├── dashboard/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   └── pages/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
│
├── services/
│   ├── seo-content/
│   ├── seo-onpage/
│   ├── seo-technical/
│   └── seo-monitor/
│
├── shared/
├── tests/
├── docs/
├── .env.example
├── docker-compose.yml
├── pytest.ini
└── README.md
```

---

# Instalación local

## 1. Clonar el repositorio

```bash
git clone https://github.com/JC-ProyectosDigitales/seo-automation-platform.git
cd seo-automation-platform
```

---

## 2. Preparar variables de entorno

El proyecto incluye:

```text
.env.example
```

En PowerShell:

```powershell
Copy-Item .env.example .env
```

En Linux:

```bash
cp .env.example .env
```

Configura las credenciales de PostgreSQL antes de iniciar los servicios.

---

## 3. Preparar la red Docker

El `docker-compose.yml` utiliza una red externa:

```text
seo-network
```

Crear la red:

```bash
docker network create seo-network
```

Si ya existe, este paso no es necesario.

---

## 4. Preparar PostgreSQL

La plataforma espera una instancia PostgreSQL accesible desde `seo-network`.

La configuración de conexión se define mediante las variables de entorno del proyecto.

---

## 5. Construir e iniciar la plataforma

```bash
docker compose up -d --build
```

Esto inicia:

```text
seo-dashboard
seo-api-gateway
seo-content-service
seo-onpage-service
seo-technical-service
seo-monitor-service
```

---

## 6. Verificar contenedores

```bash
docker compose ps
```

---

# Acceso local

### Dashboard

```text
http://localhost:5173
```

### API Gateway

```text
http://localhost:5100
```

### Swagger / OpenAPI

```text
http://localhost:5100/docs
```

### SEO Content

```text
http://localhost:5103
```

### SEO OnPage

```text
http://localhost:5104
```

### SEO Technical

```text
http://localhost:5105
```

### SEO Monitor

```text
http://localhost:5106
```

---

# Estado actual

Actualmente `main` incluye:

- Dashboard React desplegado mediante Nginx.
- API Gateway con FastAPI.
- PostgreSQL como capa de persistencia.
- Arquitectura basada en microservicios.
- SEO Content funcional.
- SEO OnPage funcional.
- SEO Technical funcional.
- SEO Monitor funcional.
- Gestión dinámica de módulos.
- Selección de módulos por auditoría.
- Priorización de servicios.
- Timeouts configurables.
- Historial de auditorías.
- Visualización detallada de resultados.
- Manejo de errores entre servicios.
- Dockerización de los componentes principales.

---

# Documentación

El repositorio incluye documentación técnica adicional dentro de:

```text
docs/
```

Entre los documentos disponibles se encuentran:

- arquitectura;
- contratos API;
- API Gateway;
- base de datos;
- despliegue;
- guía de desarrollo;
- estado del proyecto;
- documentación individual de servicios.

---

# Evolución futura

La arquitectura permite continuar incorporando funcionalidades como:

- comparación entre auditorías;
- ejecución paralela de microservicios;
- autenticación y usuarios;
- auditorías programadas;
- integración con fuentes externas de métricas;
- mejoras en visualización histórica;
- reportes y exportaciones;
- nuevos analizadores SEO.

---

# Objetivo técnico

SEO Automation Platform demuestra una arquitectura donde diferentes analizadores especializados pueden evolucionar de forma independiente mientras un Gateway común mantiene:

```text
orquestación
+
persistencia
+
prioridades
+
timeouts
+
administración
+
contratos comunes
```

Este enfoque facilita ampliar la plataforma sin convertir el backend en una aplicación monolítica.

---

## Autor

**Diego de Jesús Castillo Andrade**

Proyecto desarrollado como parte de la formación en Tecnologías de la Información y la exploración de herramientas orientadas a automatización, SEO y arquitecturas basadas en microservicios.