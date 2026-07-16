Deployment Documentation
Descripción general

SEO Automation Platform utiliza una arquitectura basada en contenedores Docker para ejecutar sus diferentes componentes.

El despliegue local utiliza Docker Compose para administrar:

API Gateway.
Servicios SEO independientes.
Base de datos.
Dashboard web.

La finalidad es permitir que cada componente pueda ejecutarse y desarrollarse de forma independiente.

Requisitos del sistema

Antes de iniciar el proyecto se requiere:

Software necesario
Docker.
Docker Compose.
Node.js.
npm.
Verificación

Comprobar instalación:
docker --version

docker compose version

node --version

npm --version

Estructura de despliegue

La plataforma está organizada de la siguiente manera:

seo-automation-platform/

│
├── api-gateway/
│
├── services/
│   │
│   ├── ai-agent/
│   ├── seo-content/
│   ├── seo-monitor/
│   ├── seo-onpage/
│   └── seo-technical/
│
├── dashboard/
│
├── database/
│
└── docker-compose.yml

Arquitectura de ejecución
                 Usuario

                    |
                    |

              Dashboard React

              localhost:5173

                    |
                    |

              API Gateway

              localhost:5000

                    |
        -------------------------
        |           |           |

 seo-onpage  seo-content  seo-technical

        |
        |

      Base de datos
Configuración mediante variables de entorno

Cada servicio puede utilizar variables de entorno mediante archivos .env.

Ejemplo:

DATABASE_URL=postgresql://usuario:password@database:5432/seo

Las variables pueden cambiar dependiendo del entorno donde se despliegue la plataforma.

Ejecución del proyecto
1. Clonar el repositorio
git clone <repository-url>

cd seo-automation-platform
2. Levantar servicios backend

Desde la raíz del proyecto:

docker compose up -d

Esto inicia los contenedores definidos en:

docker-compose.yml
3. Verificar contenedores activos

Ejecutar:

docker compose ps

Ejemplo esperado:

api-gateway       running
seo-onpage        running
seo-content       running
seo-technical    running
database          running
Ejecución del Dashboard

Ingresar al directorio:

cd dashboard

Instalar dependencias:

npm install

Ejecutar entorno de desarrollo:

npm run dev

El dashboard estará disponible en:

http://localhost:5173
Reinicio de servicios

Para reiniciar un servicio específico:

docker compose restart api-gateway

Ejemplo:

docker compose restart seo-onpage
Reconstrucción de contenedores

Cuando se modifican dependencias o Dockerfiles:

docker compose build

Después:

docker compose up -d
Visualización de logs

Para revisar errores o ejecución:

Todos los servicios:

docker compose logs

Servicio específico:

docker compose logs api-gateway

En modo seguimiento:

docker compose logs -f api-gateway
Pruebas del sistema
Verificar API Gateway

Abrir:

http://localhost:5000/docs

Debe mostrarse la documentación automática de FastAPI.

Verificar estadísticas

Endpoint:

GET /api/stats

Ejemplo:

{
    "success": true,
    "stats": {
        "total_audits":20,
        "completed_audits":19,
        "pending_audits":1,
        "active_modules":3
    }
}
Verificar historial de auditorías

Endpoint:

GET /api/audits

Devuelve la lista de auditorías registradas.

Desarrollo de nuevos servicios

Para agregar un nuevo módulo SEO:

Crear un nuevo servicio dentro de:
services/
Crear su aplicación FastAPI.
Crear Dockerfile.
Registrar el módulo dentro de la base de datos.
Agregar la configuración correspondiente en Docker Compose.
Definir el contrato API del servicio.
Objetivo del despliegue

El sistema está preparado para ejecutarse como una plataforma modular donde cada servicio SEO puede desarrollarse y desplegarse de manera independiente.

Esta estructura permite que diferentes integrantes del equipo trabajen simultáneamente en sus respectivos módulos sin afectar el funcionamiento general de la plataforma.