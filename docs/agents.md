Agents and Services
Descripción general

SEO Automation Platform utiliza una arquitectura modular basada en servicios independientes especializados en diferentes áreas del análisis SEO.

Cada agente representa un módulo encargado de procesar una parte específica de la auditoría.

Los agentes se comunican mediante APIs REST con el API Gateway, el cual coordina la ejecución y almacenamiento de resultados.

Estructura de agentes

Los servicios disponibles actualmente son:

services/

├── ai-agent
├── seo-content
├── seo-monitor
├── seo-onpage
└── seo-technical

Cada servicio tiene una responsabilidad independiente dentro del proceso de auditoría.

AI Agent
Nombre del servicio

ai-agent

Responsabilidad

El AI Agent es responsable de interpretar los resultados obtenidos por los módulos SEO y generar recomendaciones inteligentes.

Funciones principales
Analizar resultados provenientes de otros servicios.
Identificar problemas prioritarios.
Generar recomendaciones de mejora.
Resumir resultados de auditoría.
Entrada esperada

Información obtenida de los módulos SEO.

Ejemplo:

{
"seo_onpage": {
"score": 80,
"issues": []
},
"seo_content": {
"score": 90,
"issues": []
}
}

Salida esperada

Resultado procesado con recomendaciones.

Ejemplo:

{
"priority": "high",
"recommendations": [
"Improve page structure",
"Optimize keyword usage"
]
}

SEO Content Agent
Nombre del servicio

seo-content

Responsabilidad

Analizar la calidad del contenido de una página web y determinar oportunidades de optimización.

Funciones principales
Evaluar uso de palabras clave.
Analizar estructura del contenido.
Revisar extensión del contenido.
Evaluar legibilidad.
Generar recomendaciones.
Entrada esperada
URL del sitio.
Keyword objetivo.
Información de auditoría.
Salida esperada

Resultados relacionados con contenido.

Ejemplo:

{
"score": 85,
"issues": [
"Low keyword density"
],
"recommendations": [
"Increase keyword relevance"
]
}

SEO Monitor Agent
Nombre del servicio

seo-monitor

Responsabilidad

Realizar seguimiento histórico de auditorías y cambios en los resultados SEO.

Funciones principales
Registrar cambios entre auditorías.
Comparar resultados anteriores.
Identificar mejoras.
Detectar retrocesos.
Entrada esperada

Resultados históricos de auditorías.

Salida esperada

Comparación de resultados.

Ejemplo:

{
"previous_score": 70,
"current_score": 85,
"improvement": 15
}

SEO OnPage Agent
Nombre del servicio

seo-onpage

Responsabilidad

Analizar elementos internos de una página web relacionados con SEO.

Funciones principales
Validar títulos HTML.
Revisar meta description.
Analizar encabezados H1, H2, H3.
Revisar etiquetas ALT.
Detectar problemas dentro del contenido HTML.
Entrada esperada
URL del sitio.
Keyword objetivo.
Salida esperada

Resultado del análisis OnPage.

Ejemplo:

{
"score": 90,
"issues": [
"Missing H1 tag"
],
"recommendations": [
"Add a descriptive H1"
]
}

SEO Technical Agent
Nombre del servicio

seo-technical

Responsabilidad

Analizar configuraciones técnicas que afectan el posicionamiento SEO.

Funciones principales
Validar robots.txt.
Validar sitemap.xml.
Revisar configuraciones técnicas.
Detectar problemas de accesibilidad para motores de búsqueda.
Entrada esperada
URL del sitio.
Salida esperada

Resultado del análisis técnico.

Ejemplo:

{
"score": 95,
"issues": [],
"recommendations": []
}

Integración con API Gateway

Todos los agentes deben:

Exponer un endpoint REST /audit.
Recibir solicitudes del API Gateway.
Procesar únicamente su área asignada.
Retornar resultados en formato JSON.
Mantener independencia del resto de módulos.
Objetivo de los agentes

La separación por agentes permite que cada integrante del equipo pueda desarrollar un módulo específico sin afectar el funcionamiento general de la plataforma.

El API Gateway será responsable de coordinar la ejecución de los agentes y consolidar los resultados de auditoría.