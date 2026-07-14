from fastapi import FastAPI

from app.routes.audit import router as audit_router
from app.routes.audits import router as audits_router

from app.database.connection import Base, engine
from app.database import models


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="SEO Automation API Gateway",
    version="1.0"
)


app.include_router(
    audit_router,
    prefix="/api"
)

app.include_router(
    audits_router,
    prefix="/api"
)

@app.get("/")
async def root():

    return {

        "service": "api-gateway",

        "status": "running"

    }