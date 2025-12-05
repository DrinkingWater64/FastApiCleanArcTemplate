import logging
import time
from contextlib import asynccontextmanager
from http.client import responses

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.core.config import settings
from src.core.logger import get_logger, setup_logging
from src.presentation.api import products

setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("System Starting Up")
    yield
    print("System shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Path: {request.url.path} | Time: {process_time:.4f}s | Status: {response.status_code}")
    return response

app.include_router(products.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {
        "status": "active",
        "app": settings.PROJECT_NAME
    }

# Debug Entry Point
if __name__ == "__main__":
    # In production, you would run this from the command line:
    # uvicorn src.main:app --host 0.0.0.0 --port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)