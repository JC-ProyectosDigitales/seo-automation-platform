Database Documentation
Descripción general

SEO Automation Platform utiliza una base de datos relacional para almacenar la información principal del sistema.

Actualmente la base de datos contiene las entidades necesarias para administrar:

Auditorías SEO.
Módulos disponibles.
Resultados generados por los servicios.

La comunicación con la base de datos se realiza mediante SQLAlchemy dentro del API Gateway.

Modelo de datos

Actualmente existen las siguientes tablas:

audits
modules

Relación general:

                audits

                   |
                   |
              results JSON


                modules

                   |
                   |
          servicios SEO registrados
Tabla: audits
Descripción

La tabla audits almacena la información de cada auditoría creada dentro de la plataforma.

Cada registro representa una ejecución de análisis SEO sobre un sitio web.

Estructura
| Campo          | Tipo     | Descripción                              |
| -------------- | -------- | ---------------------------------------- |
| id             | Integer  | Identificador interno de la auditoría    |
| audit_id       | String   | Identificador público único de auditoría |
| website        | String   | URL del sitio analizado                  |
| keyword        | String   | Palabra clave objetivo                   |
| status         | String   | Estado actual de la auditoría            |
| results        | JSON     | Resultados generados por los módulos     |
| error_message  | String   | Mensaje de error en caso de fallo        |
| created_at     | DateTime | Fecha de creación                        |
| started_at     | DateTime | Fecha de inicio de ejecución             |
| completed_at   | DateTime | Fecha de finalización                    |
| execution_time | Float    | Tiempo total de ejecución                |


Estados de auditoría

El campo status representa el estado actual del proceso.

Estados disponibles:

pending

La auditoría fue creada pero todavía no inicia.

running

La auditoría está siendo procesada por los servicios.

completed

La auditoría terminó correctamente.

failed

La auditoría terminó con errores.

Ejemplo de registro Audit

{
"audit_id": "AUD-20260716-191541",
"website": "https://ejemplo.com",
"keyword": "seo",
"status": "completed",
"results": {
"seo-onpage": {
"score": 85
}
}
}

Tabla: modules
Descripción

La tabla modules almacena la configuración de los servicios SEO disponibles dentro del sistema.

Cada módulo representa un servicio externo que puede ser ejecutado durante una auditoría.

Estructura
| Campo       | Tipo     | Descripción                         |
| ----------- | -------- | ----------------------------------- |
| id          | Integer  | Identificador interno del módulo    |
| name        | String   | Nombre del servicio                 |
| url         | String   | Endpoint del servicio               |
| description | String   | Descripción del módulo              |
| active      | Boolean  | Indica si el módulo está habilitado |
| priority    | Integer  | Orden de ejecución                  |
| timeout     | Integer  | Tiempo máximo de espera             |
| created_at  | DateTime | Fecha de creación                   |
| updated_at  | DateTime | Última actualización                |


Ejemplo de registro Module

{
"name": "seo-onpage",
"url": "http://seo-onpage:8000",
"description": "Analizador SEO OnPage",
"active": true,
"priority": 1,
"timeout": 30
}

Ejecución de auditorías

El flujo de almacenamiento funciona de la siguiente manera:

El usuario crea una auditoría.
El API Gateway genera un identificador único (audit_id).
La auditoría se guarda con estado pending.
Los servicios SEO procesan la información.
Los resultados obtenidos se almacenan en el campo results.
El estado cambia a completed cuando finaliza correctamente.
En caso de error se almacena información en error_message.
Almacenamiento de resultados

Los resultados de los servicios se almacenan utilizando un campo JSON.

Esto permite mantener una estructura flexible debido a que cada módulo puede generar información diferente.

Ejemplo:

{
"seo-onpage": {
"score": 90,
"issues": []
},
"seo-content": {
"score": 80,
"recommendations": []
}
}

Objetivo de la base de datos

La base de datos permite centralizar la información de auditorías y módulos, manteniendo una estructura flexible que facilite la integración de nuevos servicios SEO en el futuro.