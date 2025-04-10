from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import ollama, item, merchant, keyword, review, ocr
from models import create_db_and_tables, populate_database
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    populate_database()
    yield

app = FastAPI(
    title="FastAPI Server", description="A basic FastAPI server", version="1.0.0",
    lifespan=lifespan
)

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
