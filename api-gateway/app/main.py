from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import models
from app.database.connection import Base, SessionLocal, engine
from app.database.models import Module
from app.routes.audit import router as audit_router
from app.routes.audits import router as audits_router
from app.routes.modules import router as modules_router
from app.routes.stats import router as stats_router


Base.metadata.create_all(bind=engine)


DEFAULT_MODULES = [
    {
        "name": "seo-content",
        "url": "http://seo-content:5003/audit",
        "description": "Analisis y optimizacion de contenido SEO",
        "active": True,
        "priority": 10,
        "timeout": 30,
    },
    {
        "name": "seo-onpage",
        "url": "http://seo-onpage:5004/audit",
        "description": "Analisis de elementos SEO On-Page",
        "active": True,
        "priority": 20,
        "timeout": 30,
    },
    {
        "name": "seo-technical",
        "url": "http://seo-technical:5005/audit",
        "description": "Analisis tecnico del sitio web",
        "active": True,
        "priority": 30,
        "timeout": 30,
    },
    {
        "name": "seo-monitor",
        "url": "http://seo-monitor:5006/audit",
        "description": "Monitoreo de disponibilidad y estado del sitio web",
        "active": True,
        "priority": 40,
        "timeout": 30
    },
]


def register_default_modules():
    db = SessionLocal()

    try:
        for module_data in DEFAULT_MODULES:
            existing_module = (
                db.query(Module)
                .filter(Module.name == module_data["name"])
                .first()
            )

            if existing_module is None:
                module = Module(**module_data)
                db.add(module)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_default_modules()

    yield


app = FastAPI(
    title="SEO Automation API Gateway",
    version="1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    audit_router,
    prefix="/api",
)

app.include_router(
    audits_router,
    prefix="/api",
)

app.include_router(
    modules_router,
    prefix="/api",
)

app.include_router(
    stats_router,
    prefix="/api",
)


@app.get("/")
async def root():
    return {
        "service": "api-gateway",
        "status": "running",
    }
