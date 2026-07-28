from fastapi import FastAPI

from app.routes.audit import router


app = FastAPI(
    title="SEO OnPage Service",
    version="2.0.0",
    description=(
        "Servicio de análisis SEO OnPage de la plataforma "
        "SEO Automation."
    ),
)


app.include_router(
    router,
)


@app.get("/")
def root():
    return {
        "service": "seo-onpage",
        "status": "running",
        "version": "2.0.0",
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "module": "seo-onpage",
        "status": "healthy",
    }
