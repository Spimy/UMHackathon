from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from __init__ import create_db

from routes import (
    ollama,
)
import uvicorn

app = FastAPI(
    title="FastAPI Server", description="A basic FastAPI server", version="1.0.0"
)

app.include_router(ollama.router)

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
    create_db()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
