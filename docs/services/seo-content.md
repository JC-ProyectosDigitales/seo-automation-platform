# Servicio SEO Content

## Descripción

El servicio SEO Content es responsable de analizar la calidad del contenido de una página web y detectar oportunidades de mejora relacionadas con relevancia, estructura, legibilidad y optimización para motores de búsqueda.

Este servicio será utilizado por el API Gateway durante la ejecución de una auditoría SEO.


---

# Responsabilidad del servicio

El servicio debe analizar:

- Calidad del contenido textual.
- Longitud del contenido.
- Relevancia respecto a la palabra clave objetivo.
- Uso de palabras clave.
- Legibilidad del texto.
- Distribución de términos importantes.
- Oportunidades de generación o mejora de contenido.


---

# Arquitectura

Flujo de comunicación:

Dashboard
|
v
API Gateway
|
v
seo-content
|
v
Resultado del análisis



El servicio no debe tener comunicación directa con el dashboard.

Toda solicitud debe realizarse mediante el API Gateway.


---

# Endpoint requerido

## Ejecutar auditoría de contenido


Método:


POST



Ruta:


/audit



---

# Request


Ejemplo:

```json
{
    "audit_id": "AUD-20260716-001",
    "website": "https://ejemplo.com",
    "keyword": "marketing digital"
}

Campos:

| Campo    | Tipo   | Descripción                      |
| -------- | ------ | -------------------------------- |
| audit_id | string | Identificador único de auditoría |
| website  | string | URL del sitio a analizar         |
| keyword  | string | Palabra clave objetivo           |

Response

Ejemplo:

{
    "success": true,
    "module": "seo-content",
    "audit_id": "AUD-20260716-001",
    "score": 78,
    "analysis": {
        "word_count": 850,
        "keyword_density": 2.5,
        "readability": "medium"
    },
    "issues": [
        {
            "type": "warning",
            "message": "El contenido tiene poca extensión"
        }
    ],
    "recommendations": [
        "Incrementar profundidad del contenido",
        "Agregar términos relacionados"
    ]
}
Datos esperados del análisis

El servicio puede evaluar:

Longitud del contenido

Ejemplo:

Menos de 300 palabras → posible contenido insuficiente.
Entre 300 y 1000 palabras → contenido aceptable.
Más de 1000 palabras → contenido extenso.
Palabra clave

Debe analizar:

Presencia del término principal.
Frecuencia de aparición.
Distribución dentro del contenido.
Legibilidad

Puede considerar:

Longitud de frases.
Uso de párrafos.
Complejidad del texto.
Estados posibles
Auditoría completada
{
    "status": "completed"
}
Error
{
    "status": "error",
    "message": "Descripción del error"
}
Integración con API Gateway

El API Gateway enviará:

Identificador de auditoría.
URL del sitio.
Keyword objetivo.

El servicio responderá:

Puntuación del contenido.
Problemas encontrados.
Recomendaciones.
Restricciones

El servicio debe:

Utilizar REST API.
Utilizar JSON.
No acceder directamente a la base de datos.
No depender del dashboard.
Mantener compatibilidad con el contrato general de auditorías.