from fastapi import FastAPI

from app.routes.audit import router


app = FastAPI(
    title="SEO Monitor Service",
    version="2.0.0",
    description=(
        "Servicio de monitoreo de disponibilidad, "
        "rendimiento HTTP y certificado SSL."
    ),
)


app.include_router(
    router
)


@app.get("/")
def root():
    return {
        "service": "seo-monitor",
        "status": "running",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "module": "seo-monitor",
        "status": "healthy",
    }
