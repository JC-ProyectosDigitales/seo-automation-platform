# Team Assignment

## Descripción

Este documento define la distribución de trabajo para el desarrollo de los servicios que forman parte de SEO Automation Platform.

Cada integrante será responsable de desarrollar un servicio independiente siguiendo los contratos definidos por la plataforma.

Todos los servicios deben comunicarse mediante el API Gateway y respetar la estructura de respuestas establecida.

---

# Arquitectura de trabajo

La plataforma se divide en:

Dashboard
|
|
API Gateway
|
+----------------+
| | |
v v v

SEO Content
SEO OnPage
SEO Technical

|
v

AI Agent


---

# Responsabilidades generales

Todos los integrantes deben:

- Mantener su servicio independiente.
- Utilizar FastAPI.
- Crear su propio Dockerfile.
- Mantener requirements.txt actualizado.
- Exponer endpoint `/audit`.
- Responder utilizando JSON estándar.
- Documentar cambios realizados.
- Probar el servicio antes de integrarlo.

---

# Servicio: SEO Content

## Objetivo

Analizar aspectos relacionados con la calidad y optimización del contenido de una página web.

---

## Responsabilidades

El servicio debe analizar:

- Calidad del contenido.
- Uso de palabras clave.
- Relevancia del texto.
- Extensión del contenido.
- Estructura básica del contenido.

---

## Endpoint requerido


POST /audit


Entrada:

{
    "audit_id": "AUD-001",
    "website": "https://ejemplo.com",
    "keyword": "seo"
}

Salida esperada:

{
    "success": true,
    "service": "seo-content",
    "data": {
        "score": 80,
        "recommendations": []
    },
    "error": null
}

## Servicio: SEO OnPage

### Objetivo

Analizar elementos internos de una página web.

## Responsabilidades

Debe analizar:

- Etiqueta title.
- Meta description.
- Encabezados HTML.
- Etiquetas H1.
- Imágenes ALT.
- Estructura HTML.

## Endpoint requerido

POST /audit

Entrada:

{
    "audit_id": "AUD-001",
    "website": "https://ejemplo.com",
    "keyword": "seo"
}

Salida esperada:

{
    "success": true,
    "service": "seo-onpage",
    "data": {
        "issues": [],
        "score": 90
    },
    "error": null
}


## Servicio: SEO Technical

### Objetivo

Analizar configuraciones técnicas que afectan el posicionamiento.

## Responsabilidades

Debe analizar:

- robots.txt.
- sitemap.xml.
- Estado HTTP.
- Velocidad básica.
- Configuración técnica.

## Endpoint requerido
POST /audit

Salida esperada:

{
    "success": true,
    "service": "seo-technical",
    "data": {
        "technical_score": 85
    },
    "error": null
}


## Servicio: SEO Monitor

### Objetivo

Realizar seguimiento de métricas SEO.

## Responsabilidades

Debe encargarse de:

- Historial de auditorías.
- Seguimiento de cambios.
- Comparación de resultados.

## Servicio: AI Agent

### Objetivo

Utilizar modelos de inteligencia artificial para generar recomendaciones.

## Responsabilidades

Debe procesar:

- Resultados de auditorías.
- Problemas encontrados.
- Recomendaciones SEO.

Salida esperada:

{
    "success": true,
    "service": "ai-agent",
    "data": {
        "recommendations": []
    },
    "error": null
}

## Integración con API Gateway

El flujo esperado:

1. Usuario crea auditoría.

2. Dashboard envía solicitud al API Gateway.

3. API Gateway crea registro en base de datos.

4. API Gateway ejecuta servicios SEO.

5. Servicios regresan resultados.

6. API Gateway almacena resultados.

7. Dashboard muestra información.

## Criterios de entrega

Cada servicio debe entregar:

### Código
- Código fuente completo.
- Dockerfile.
- requirements.txt.
### API
- Endpoint /audit.
- Documentación Swagger.
- Pruebas básicas.
### Integración
- Servicio registrado en API Gateway.
- Respuesta compatible.
- Comunicación mediante Docker.

## Estado del proyecto

### Completado actualmente
 - Arquitectura base.
 - API Gateway.
 - Dashboard inicial.
 - Gestión de auditorías.
 - Historial de auditorías.
 - Métricas generales.
 - Registro de módulos.

### Pendiente
 - Desarrollo interno de servicios SEO.
 - Integración completa de módulos.
 - Ejecución real de auditorías.
 - Generación avanzada de recomendaciones.


## Objetivo final

Permitir que diferentes integrantes desarrollen servicios especializados de forma independiente, manteniendo una arquitectura modular y escalable.