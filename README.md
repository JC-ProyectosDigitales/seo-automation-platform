# SEO Automation Platform

Plataforma web basada en una arquitectura de microservicios para automatizar auditorías SEO iniciales sobre sitios web reales.

La aplicación analiza automáticamente aspectos relacionados con contenido, optimización On-Page, configuración técnica y monitoreo del sitio, generando recomendaciones para mejorar el posicionamiento en motores de búsqueda.

---

## Características

- Auditoría SEO de sitios web reales.
- Arquitectura basada en microservicios.
- API Gateway desarrollado con FastAPI.
- Dashboard desarrollado con React.
- Persistencia de auditorías en PostgreSQL.
- Comunicación entre servicios mediante APIs REST.
- Ejecución independiente de módulos SEO.
- Historial de auditorías.
- Visualización detallada de resultados.
- Despliegue mediante Docker Compose.

---

## Arquitectura

```
                +----------------+
                | React Dashboard|
                +-------+--------+
                        |
                        |
                 API Gateway
                 (FastAPI)
                        |
    +-----------+-------+---------+-----------+
    |           |                 |           |
SEO Content  SEO OnPage   SEO Technical  SEO Monitor
    |           |                 |           |
    +-----------+-------+---------+-----------+
                        |
                  PostgreSQL
```

---

## Tecnologías utilizadas

### Frontend

- React
- React Router
- Vite

### Backend

- FastAPI
- Python

### Base de datos

- PostgreSQL

### Infraestructura

- Docker
- Docker Compose
- Nginx

---

## Microservicios

### SEO Content

Analiza:

- Palabra clave principal
- Encabezados H1, H2 y H3
- Legibilidad
- SEO Title
- Meta Description
- Densidad de palabras clave
- Recomendaciones de contenido

### SEO OnPage

Analiza:

- Meta etiquetas
- Open Graph
- Canonical
- Imágenes
- Texto ALT
- Enlaces internos
- Enlaces externos

### SEO Technical

Analiza:

- HTTPS
- robots.txt
- sitemap.xml
- Estado HTTP
- Tiempo de respuesta
- Meta Robots

### SEO Monitor

Analiza:

- Disponibilidad del sitio
- Certificado SSL
- Redirecciones
- Tiempo de respuesta
- Estado del servidor

---

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/USUARIO/seo-automation-platform.git

cd seo-automation-platform
```

### Levantar la aplicación

```bash
docker compose up --build
```

---

## Acceso

Dashboard

```
http://localhost:5173
```

API Gateway

```
http://localhost:5100
```

Health Check

```
http://localhost:5100/health
```

---

## Flujo de funcionamiento

1. El usuario ingresa una URL y una palabra clave.
2. El Dashboard envía la solicitud al API Gateway.
3. El Gateway distribuye la auditoría entre los microservicios.
4. Cada módulo realiza su análisis de manera independiente.
5. Los resultados son almacenados en PostgreSQL.
6. El Dashboard consulta la auditoría final.
7. Se presentan métricas, problemas y recomendaciones.

---

## Estructura del proyecto

```
seo-automation-platform/
│
├── api-gateway/
├── dashboard/
├── database/
├── nginx/
├── services/
│   ├── seo-content/
│   ├── seo-onpage/
│   ├── seo-technical/
│   └── seo-monitor/
│
├── docker-compose.yml
└── README.md
```

---

## Estado del proyecto

Actualmente la plataforma implementa:

- Auditorías SEO sobre sitios web reales.
- API Gateway con FastAPI.
- Arquitectura de microservicios.
- Dashboard desarrollado en React.
- Historial de auditorías.
- Persistencia en PostgreSQL.
- Comunicación REST entre servicios.
- Despliegue mediante Docker Compose.

---

## Próximas mejoras

- Exportación de auditorías en PDF.
- Comparación entre auditorías.
- Integración con Google Search Console.
- Integración con Google Analytics.
- Programación de auditorías periódicas.
- Panel de estadísticas.
- Reportes descargables.

---

## Autor

Desarrollado como proyecto académico para la carrera de Ingeniería en Tecnologías de la Información.

**Autor:** Zonick von Mauss

Universidad Tecnológica del Centro de Veracruz
