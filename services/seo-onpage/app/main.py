from fastapi import FastAPI
from app.routes.audit import router


app = FastAPI(
    title="SEO OnPage Service",
    version="1.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "service": "seo-onpage",
        "status": "running"
    }