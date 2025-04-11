from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from routes import ollama, item, merchant, keyword, review, ocr
from models import create_db_and_tables, populate_database
import uvicorn
import os
import pathlib

# Create uploads directory before app initialization
UPLOADS_DIR = pathlib.Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    populate_database()
    yield

app = FastAPI(
    title="FastAPI Server", description="A basic FastAPI server", version="1.0.0",
    lifespan=lifespan
)

# Mount the uploads directory using absolute path
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

app.include_router(ollama.router)
app.include_router(item.router)
app.include_router(merchant.router)
app.include_router(review.router)
app.include_router(keyword.router)
app.include_router(ocr.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
