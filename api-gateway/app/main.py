from fastapi import FastAPI

from app.routes.audit import router as audit_router


app = FastAPI(
    title="SEO Automation API Gateway",
    version="1.0"
)


app.include_router(
    audit_router,
    prefix="/api"
)


@app.get("/")
async def root():

    return {

        "service":"api-gateway",

        "status":"running"

    }