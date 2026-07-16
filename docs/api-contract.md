API Contract
Descripción general

Este documento define el contrato de comunicación entre el API Gateway y los servicios SEO que forman parte de la plataforma SEO Automation Platform.

La comunicación entre componentes utiliza APIs REST con intercambio de información en formato JSON.

El API Gateway funciona como punto central de comunicación entre el Dashboard y los servicios especializados de análisis SEO.

Cada servicio SEO debe cumplir con este contrato para poder integrarse correctamente con la plataforma.

Arquitectura de comunicación

El flujo general de comunicación es:

Dashboard → API Gateway → Servicio SEO → Resultado → API Gateway → Dashboard

El usuario inicia una auditoría desde el Dashboard.

El API Gateway registra la auditoría, consulta los módulos activos y envía solicitudes a los servicios correspondientes.

Cada servicio procesa la información recibida y devuelve sus resultados al Gateway.

Endpoint estándar de servicios SEO

Cada servicio SEO debe exponer un endpoint para recibir solicitudes de auditoría.

Método

POST

Ruta

/audit

Solicitud (Request)

El API Gateway enviará la información de la auditoría mediante JSON.

Ejemplo:

{
"audit_id": "AUD-20260716-191541",
"website": "https://ejemplo.com",
"keyword": "seo"
}

Parámetros
| Campo    | Tipo   | Descripción                            |
| -------- | ------ | -------------------------------------- |
| audit_id | string | Identificador único de la auditoría    |
| website  | string | URL del sitio web que será analizado   |
| keyword  | string | Palabra clave objetivo de la auditoría |



Respuesta (Response)

Cada servicio debe devolver un resultado en formato JSON.

Ejemplo:

{
"success": true,
"service": "seo-onpage",
"score": 85,
"issues": [],
"recommendations": []
}

Parámetros de respuesta
| Campo    | Tipo   | Descripción                            |
| -------- | ------ | -------------------------------------- |
| audit_id | string | Identificador único de la auditoría    |
| website  | string | URL del sitio web que será analizado   |
| keyword  | string | Palabra clave objetivo de la auditoría |


Estructura de resultados

Cada servicio es responsable de generar resultados relacionados con su área de análisis.

Ejemplo de resultado:

{
"service": "seo-technical",
"score": 90,
"issues": [
{
"type": "warning",
"message": "Missing sitemap.xml"
}
],
"recommendations": [
"Create and register sitemap.xml"
]
}

Servicios registrados
seo-onpage

Responsabilidad:

Analizar elementos internos de una página web.

Funciones principales:

Revisión de etiquetas HTML.
Evaluación de títulos.
Validación de meta descriptions.
Análisis de encabezados.
Revisión de atributos ALT en imágenes.
seo-content

Responsabilidad:

Evaluar la calidad y optimización del contenido.

Funciones principales:

Análisis de palabras clave.
Evaluación de estructura del contenido.
Revisión de legibilidad.
Generación de recomendaciones.
seo-technical

Responsabilidad:

Analizar configuraciones técnicas del sitio web.

Funciones principales:

Validación de robots.txt.
Validación de sitemap.xml.
Revisión de aspectos técnicos SEO.
Identificación de problemas de configuración.
seo-monitor

Responsabilidad:

Realizar seguimiento de auditorías y cambios.

Funciones principales:

Guardar historial de resultados.
Comparar auditorías.
Identificar mejoras o retrocesos.
ai-agent

Responsabilidad:

Procesar resultados SEO y generar recomendaciones inteligentes.

Funciones principales:

Interpretación de resultados.
Priorización de problemas.
Generación de sugerencias.
Manejo de errores

Cuando un servicio no pueda completar una auditoría debe responder indicando el error.

Ejemplo:

{
"success": false,
"service": "seo-content",
"error": "Unable to analyze website"
}

Códigos de error
| Campo           | Tipo    |  Descripción                                 |
| --------------- | ------- | ------------------------------------------- |
| success         | boolean | Indica si el análisis terminó correctamente |
| service         | string  | Nombre del módulo que generó el resultado   |
| score           | integer | Puntuación obtenida en el análisis          |
| issues          | array   | Lista de problemas encontrados              |
| recommendations | array   | Lista de recomendaciones                    |


Reglas de integración

Todos los servicios deben cumplir con las siguientes reglas:

Utilizar comunicación HTTP REST.
Recibir datos en formato JSON.
Responder datos en formato JSON.
Mantener la estructura definida del contrato.
Informar errores mediante respuestas controladas.
Respetar los tiempos de ejecución configurados desde el Gateway.
Objetivo del contrato

Definir una comunicación estándar entre el API Gateway y los servicios SEO, permitiendo que cada integrante pueda desarrollar su módulo de manera independiente y posteriormente integrarlo a la plataforma principal.