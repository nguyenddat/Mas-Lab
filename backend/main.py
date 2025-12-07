import os

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from core import config
from routers import paper_router

def get_application() -> FastAPI:
    application = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)
    
    # Thêm static dir là artifacts
    application.mount("/static", StaticFiles(directory="artifacts"), name="static")

    application.include_router(paper_router, prefix="/api", tags=["paper"])
    return application

app = get_application()