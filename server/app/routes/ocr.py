import base64
from google import genai
from google.genai import types
import os
import dotenv
from scan import DocScanner
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

dotenv.load_dotenv()

router = APIRouter()

@router.post("/OCR/generate")
def generate(image: str = "input") -> StreamingResponse:
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    scanner = DocScanner()
    encoded_string = scanner.scan("../../../shared/images/{image}.jpg")

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type="""image/jpeg""",
                    data=base64.b64decode(encoded_string),
                ),
                types.Part.from_text(
                    text="""
                    You are an advanced OCR and text formatting assistant. Your task is to extract text from an image-based document and reformat it into consistent paragraphs. The input will be an image containing text. The extracted text may have unnecessary line breaks within paragraphs, but true paragraph breaks are separated by blank lines. Your goal is to:

                    1. Perform OCR on the image to extract the text.
                    2. Merge lines within the same paragraph into a single continuous block of text.
                    3. Preserve blank lines that separate different paragraphs.
                    4. Ignore page numbers
                    
                    Here is an example of the input and the desired output:
                    
                    Input:

                    ```
                    The fox jumps over the lazy dog. Foxes are clever animals. 
                    They can be found in various habitats, including forests, 
                    grasslands, and even urban areas.
                    
                    However, they are often misunderstood and seen as pests.
                    Poor foxes.
                    ```
                    
                    Output:
                    
                    ```
                    The fox jumps over the lazy dog. Foxes are clever animals. They can be found in various habitats, including forests, grasslands, and even urban areas.
                    
                    However, they are often misunderstood and seen as pests. Poor foxes.
                    ```
                    
                    Task: Reformat the extracted text into consistent paragraphs as shown in the example above. Ensure that lines within the same paragraph are merged into one block, and blank lines between paragraphs are preserved.
                    """),
            ],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    def generate_stream():
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            yield chunk.content.parts[0].text

    return StreamingResponse(generate_stream(), media_type="text/plain")
