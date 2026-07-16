Arquitectura del Sistema
1. Introducción

SEO Automation Platform es una plataforma modular orientada a la automatización de procesos de optimización SEO mediante servicios independientes.

El sistema está diseñado utilizando una arquitectura basada en microservicios, donde cada módulo SEO funciona como un servicio separado encargado de analizar un área específica de optimización.

La arquitectura busca permitir:

Desarrollo independiente de cada módulo.
Escalabilidad de servicios.
Separación de responsabilidades.
Integración sencilla de nuevos analizadores SEO.
Trabajo paralelo entre diferentes integrantes del equipo.
2. Arquitectura general

La plataforma está compuesta por los siguientes componentes principales:

Dashboard Web.
API Gateway.
Servicios SEO especializados.
Base de datos.
Sistema de comunicación entre servicios.

La estructura general es:

Usuario
   |
   |
Dashboard Web
(React)
   |
   |
API Gateway
(FastAPI)
   |
   |
--------------------------------
|        |          |           |
SEO     SEO        SEO        AI
OnPage Content   Technical  Agent
Service Service  Service   Service
   |
   |
Base de Datos
3. Componentes del sistema
3.1 Dashboard Web
Tecnología
React.
Vite.
Axios.
React Router.
Responsabilidad

El Dashboard representa la interfaz utilizada por el usuario final para interactuar con la plataforma.

Sus funciones principales son:

Crear auditorías SEO.
Consultar resultados.
Visualizar historial de auditorías.
Mostrar métricas generales.
Consultar módulos disponibles.

El Dashboard no realiza análisis SEO directamente.

Todas las operaciones son realizadas mediante comunicación con el API Gateway.

3.2 API Gateway
Tecnología
FastAPI.
Python.
SQLAlchemy.
Responsabilidad

El API Gateway funciona como punto central de comunicación entre el Dashboard y los servicios internos.

Sus funciones principales son:

Recibir solicitudes del usuario.
Gestionar auditorías.
Registrar información en la base de datos.
Coordinar la ejecución de módulos.
Entregar resultados procesados al Dashboard.

Ejemplos de operaciones:

Crear auditoría
Consultar auditorías
Consultar resultados
Obtener estadísticas
Gestionar módulos
3.3 Servicios SEO

Los servicios SEO funcionan como módulos independientes.

Cada servicio tiene:

Su propia aplicación FastAPI.
Sus propias rutas.
Sus propias responsabilidades.
Comunicación mediante API REST.

Actualmente la estructura contempla:

services/

├── ai-agent
├── seo-content
├── seo-monitor
├── seo-onpage
└── seo-technical
4. Módulos SEO
4.1 SEO OnPage

Responsable del análisis de elementos internos de una página web.

Ejemplos:

Etiquetas HTML.
Titles.
Meta descriptions.
Encabezados.
Estructura del contenido.
Uso de palabras clave.
4.2 SEO Content

Responsable del análisis relacionado con contenido.

Ejemplos:

Calidad del contenido.
Relevancia de palabras clave.
Legibilidad.
Estructura textual.
Recomendaciones de mejora.
4.3 SEO Technical

Responsable de auditorías técnicas del sitio.

Ejemplos:

Sitemap.
Robots.txt.
Código HTTP.
Rendimiento.
Configuración técnica.
4.4 SEO Monitor

Responsable del seguimiento y monitoreo de métricas SEO.

Ejemplos:

Cambios en posiciones.
Estado del sitio.
Seguimiento histórico.
4.5 AI Agent

Responsable de integrar capacidades de inteligencia artificial.

Posibles funciones:

Generación de recomendaciones.
Interpretación de resultados SEO.
Priorización de mejoras.
5. Comunicación entre servicios

La comunicación interna utiliza APIs REST utilizando formato JSON.

Ejemplo de solicitud:

{
    "website": "https://ejemplo.com",
    "keyword": "marketing digital"
}

Ejemplo de respuesta:

{
    "module": "seo-onpage",
    "status": "completed",
    "result": {
        "score": 85,
        "recommendations": []
    }
}
6. Flujo de ejecución de una auditoría

El flujo general es:

Paso 1

El usuario introduce un sitio web desde el Dashboard.

Paso 2

El Dashboard envía la solicitud al API Gateway.

Paso 3

El API Gateway crea un registro de auditoría.

Ejemplo:

status = pending
Paso 4

El API Gateway ejecuta los módulos SEO configurados.

Ejemplo:

SEO OnPage
SEO Content
SEO Technical
Paso 5

Cada módulo procesa la información y devuelve resultados.

Paso 6

El API Gateway almacena los resultados.

Estado final:

status = completed
Paso 7

El Dashboard muestra:

Estado.
Resultados.
Recomendaciones.
Métricas.
7. Base de datos

La plataforma utiliza una base de datos relacional para almacenar información del sistema.

Actualmente maneja principalmente:

Tabla Audit

Almacena las auditorías realizadas.

Contiene:

Identificador de auditoría.
Sitio analizado.
Palabra clave.
Estado.
Resultados.
Fechas de ejecución.
Tabla Module

Almacena la configuración de los módulos disponibles.

Contiene:

Nombre.
URL del servicio.
Estado activo.
Prioridad.
Tiempo máximo de ejecución.
8. Contenedores Docker

Cada servicio se ejecuta dentro de un contenedor independiente.

Ejemplo:

Docker Compose

|
├── api-gateway
|
├── seo-onpage
|
├── seo-content
|
├── seo-technical
|
└── database

Ventajas:

Entornos aislados.
Fácil instalación.
Desarrollo independiente.
Escalabilidad futura.
9. Principios de diseño

La arquitectura sigue los siguientes principios:

Modularidad

Cada módulo SEO puede evolucionar independientemente.

Separación de responsabilidades

Cada componente tiene una función específica.

Escalabilidad

Los servicios pueden crecer o replicarse según la demanda.

Integración sencilla

Los nuevos módulos pueden agregarse mediante contratos API definidos.

10. Objetivo de la arquitectura

La arquitectura propuesta permite construir una plataforma SEO automatizada donde diferentes integrantes pueden desarrollar módulos independientes mientras mantienen una integración común mediante APIs REST.

Esta estructura facilita la colaboración del equipo y permite evolucionar la plataforma hacia una solución más completa sin modificar los componentes existentes.