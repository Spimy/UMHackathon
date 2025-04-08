from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ollama
from pydantic import BaseModel

router = APIRouter()


class Prompt(BaseModel):
    prompt: str


@router.post("/ollama/generate")
async def generate(prompt: Prompt) -> StreamingResponse:
    async def generate_stream():
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt.prompt}],
            stream=True,
        )

        for chunk in response:
            if chunk.message:
                yield chunk.message.content

    return StreamingResponse(generate_stream(), media_type="text/event-stream")
