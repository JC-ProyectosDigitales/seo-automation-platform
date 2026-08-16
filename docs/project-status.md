# Estado actual del proyecto

## SEO Automation Platform

Este documento resume el estado real de desarrollo de SEO Automation Platform en la rama `main`.

---

# 1. Estado general

La plataforma funciona actualmente mediante una arquitectura basada en microservicios.

El API Gateway centraliza la comunicación entre:

- Dashboard web;
- PostgreSQL;
- servicios SEO especializados.

Estado general:

| Componente | Estado |
|---|---|
| Dashboard Web | Funcional |
| API Gateway | Funcional |
| PostgreSQL | Funcional |
| Gestión de auditorías | Funcional |
| Historial de auditorías | Funcional |
| Consulta detallada de auditorías | Funcional |
| Estadísticas | Funcional |
| Gestión de módulos | Funcional |
| Selección de módulos | Funcional |
| SEO Content | Funcional |
| SEO OnPage | Funcional |
| SEO Technical | Funcional |
| SEO Monitor | Funcional |

---

# 2. Dashboard

El Dashboard está desarrollado con:

- React;
- React Router;
- Vite;
- Axios.

Dentro de Docker se distribuye mediante Nginx.

Actualmente permite:

- crear auditorías;
- consultar resultados;
- visualizar historial;
- abrir auditorías individuales;
- visualizar métricas;
- consultar módulos registrados;
- mostrar resultados generados por los servicios SEO.

Puerto publicado:

```text
5173
```

3. API Gateway

El API Gateway está desarrollado con FastAPI.

Sus responsabilidades actuales incluyen:

recibir solicitudes del Dashboard;
crear auditorías;
generar identificadores;
almacenar información en PostgreSQL;
obtener módulos activos;
filtrar módulos seleccionados;
ejecutar microservicios;
aplicar prioridad;
aplicar timeout;
detectar módulos no disponibles;
consolidar respuestas;
guardar resultados;
mantener historial;
exponer estadísticas;
administrar módulos.

Puerto publicado:

5100

Swagger:

http://localhost:5100/docs
4. Módulos registrados por defecto

Actualmente el API Gateway registra automáticamente los siguientes módulos cuando todavía no existen en PostgreSQL:

| Módulo          | URL interna                       | Prioridad | Timeout |
| --------------- | --------------------------------- | --------: | ------: |
| `seo-content`   | `http://seo-content:5003/audit`   |        10 |    30 s |
| `seo-onpage`    | `http://seo-onpage:5004/audit`    |        20 |    30 s |
| `seo-technical` | `http://seo-technical:5005/audit` |        30 |    30 s |
| `seo-monitor`   | `http://seo-monitor:5006/audit`   |        40 |    30 s |

5. Selección de módulos

El orquestador permite:

ejecutar todos los módulos activos;
ejecutar únicamente módulos seleccionados.

Si un módulo solicitado:

no existe;
está inactivo;
no está disponible;

el Gateway genera una respuesta controlada con:

MODULE_NOT_AVAILABLE

Esto evita que una auditoría falle completamente por un módulo inexistente.

6. Estados de auditoría

El flujo de ejecución utiliza estados como:

pending
running
completed
failed

Durante el procesamiento se almacenan datos como:

fecha de creación;
fecha de inicio;
fecha de finalización;
tiempo de ejecución;
resultados;
mensaje de error cuando corresponde.
7. Base de datos

La plataforma utiliza PostgreSQL.

Las entidades principales son:

audits

Almacena:

identificador interno;
audit_id;
sitio web;
keyword;
estado;
resultados;
errores;
fechas;
tiempo de ejecución.
modules

Almacena:

nombre;
URL;
descripción;
estado activo;
prioridad;
timeout;
fechas de creación y actualización.

Los resultados de cada servicio pueden almacenarse como JSON.

8. SEO Content

Estado:

Funcional

Actualmente procesa contenido real obtenido desde una URL o contenido suministrado.

Incluye análisis relacionados con:

keyword objetivo;
estructura de contenido;
encabezados;
densidad de keyword;
legibilidad;
metadatos;
score SEO;
issues;
recomendaciones.

Puerto interno:

5003

Puerto publicado:

5103
9. SEO OnPage

Estado:

Funcional

Utiliza un analizador propio para revisar elementos SEO internos de una página.

La respuesta contiene:

score;
análisis;
issues;
recomendaciones;
errores.

Su dominio incluye elementos como:

metadatos;
títulos;
encabezados;
imágenes;
atributos ALT;
enlaces;
optimización On-Page.

Puerto interno:

5004

Puerto publicado:

5104
10. SEO Technical

Estado:

Funcional

Actualmente analiza:

HTTPS;
estado HTTP;
tiempo de respuesta;
robots.txt;
sitemap.xml;
redirecciones;
canonical;
meta robots.

La respuesta incluye:

score;
análisis técnico;
issues;
recomendaciones;
errores.

Puerto interno:

5005

Puerto publicado:

5105
11. SEO Monitor

Estado:

Funcional

El servicio analiza el estado operativo del sitio.

Actualmente evalúa:

disponibilidad;
tiempo de respuesta;
redirecciones;
código HTTP;
tipo de contenido;
tamaño de respuesta;
servidor;
certificado SSL.

También genera:

score;
issues;
recomendaciones;
errores.

Puerto interno:

5006

Puerto publicado:

5106
12. Docker

La plataforma utiliza Docker Compose para ejecutar:

seo-dashboard
seo-api-gateway
seo-content-service
seo-onpage-service
seo-technical-service
seo-monitor-service

Los servicios utilizan la red externa:

seo-network
13. Flujo actual de una auditoría
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
  +--> registra auditoría
  |
  +--> obtiene módulos activos
  |
  +--> filtra módulos seleccionados
  |
  +--> ejecuta módulos por prioridad
  |
  v
Resultados consolidados
  |
  v
PostgreSQL
  |
  v
Dashboard
14. Funcionalidades implementadas

Actualmente main incluye:

arquitectura de microservicios;
Dashboard React;
API Gateway FastAPI;
PostgreSQL;
Docker Compose;
Nginx para frontend;
auditorías sobre sitios reales;
módulos SEO independientes;
selección de módulos;
priorización;
timeouts;
historial;
detalle de auditorías;
estadísticas;
gestión de módulos;
manejo de errores entre servicios;
consolidación de resultados.
15. Pendientes y evolución futura

Las principales oportunidades de mejora son:

ampliar cobertura de pruebas;
ejecutar microservicios en paralelo;
mejorar visualización histórica;
agregar comparación entre auditorías;
incorporar autenticación y usuarios;
agregar auditorías programadas;
integrar nuevas fuentes externas de métricas;
ampliar reportes y exportaciones;
mejorar observabilidad de servicios;
preparar despliegue de producción.
16. Objetivo de evolución

La siguiente etapa ya no consiste en crear la arquitectura base, sino en ampliar capacidades sobre una plataforma funcional.

El foco puede orientarse a:

aumentar profundidad de análisis;
mejorar experiencia de usuario;
ampliar automatización;
incorporar nuevas fuentes de datos;
optimizar rendimiento;
fortalecer pruebas e infraestructura.