from fastapi import FastAPI

from app.routes.audit import router as audit_router


app = FastAPI(
    title="SEO Technical Service",
    description="Microservicio de auditoría técnica SEO.",
    version="2.0.0"
)


app.include_router(audit_router)


@app.get("/")
def root():
    return {
        "success": True,
        "service": "seo-technical",
        "version": "2.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "module": "seo-technical",
        "status": "healthy"
    }
