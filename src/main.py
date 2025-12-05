from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.config import settings
from src.presentation.api import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("System Starting Up")
    yield
    print("System shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

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