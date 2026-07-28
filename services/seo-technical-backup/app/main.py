from fastapi import FastAPI
from app.routes.audit import router


app = FastAPI(
    title="SEO Technical Service",
    version="1.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "service": "seo-technical",
        "status": "running"
    }
