from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.core.config import settings
from src.core.logger import setup_logging
from src.api.v1.auth import router as auth_router
from src.api.v1.investigations import router as investigations_router

# Setup custom loguru logger
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for the Human Digital Footprint Tracker",
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(investigations_router, prefix="/api/v1/investigations", tags=["investigations"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.PROJECT_NAME} started")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "personagraph-api"}
