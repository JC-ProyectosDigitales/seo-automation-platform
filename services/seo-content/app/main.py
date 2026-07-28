from fastapi import FastAPI

from app.routes.audit import router


app = FastAPI(
    title="SEO Content Service",
    version="2.0.0",
    description=(
        "Servicio para analizar palabras clave, estructura, "
        "legibilidad y optimización del contenido."
    ),
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "seo-content",
        "status": "running",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "module": "seo-content",
        "status": "healthy",
    }
