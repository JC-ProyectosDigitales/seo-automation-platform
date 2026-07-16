from fastapi import FastAPI

from app.routes.audit import router as audit_router
from app.routes.audits import router as audits_router
from app.routes.modules import router as modules_router
from app.routes.stats import router as stats_router

from app.database.connection import Base, engine
from app.database import models

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="SEO Automation API Gateway",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    audit_router,
    prefix="/api"
)


app.include_router(
    audits_router,
    prefix="/api"
)


app.include_router(
    modules_router,
    prefix="/api"
)

app.include_router(
    stats_router,
    prefix="/api"
)


@app.get("/")
async def root():

    return {

        "service": "api-gateway",

        "status": "running"

    }