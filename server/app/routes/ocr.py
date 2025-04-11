import base64
import os
import pathlib
import time
import uuid
from google import genai
from google.genai import types
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from settings import GEMINI_API_KEY

router = APIRouter(tags=["OCR"])

# Get the absolute path to the uploads directory
UPLOADS_DIR = pathlib.Path(__file__).parent.parent.parent / "uploads"


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename by adding timestamp and UUID if needed."""
    # Get the file extension
    name, ext = os.path.splitext(original_filename)

    # Generate unique filename with timestamp and UUID
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    new_filename = f"{name}_{timestamp}_{unique_id}{ext}"

    return new_filename


@router.post("/ocr/generate")
def generate(image: UploadFile) -> StreamingResponse:
    # Generate a unique filename
    unique_filename = generate_unique_filename(image.filename)
    file_path = UPLOADS_DIR / unique_filename

    # Save the uploaded file using absolute path
    with open(file_path, "wb") as f:
        f.write(image.file.read())

    # Reset file pointer to beginning for OCR processing
    image.file.seek(0)

    client = genai.Client(
        api_key=GEMINI_API_KEY,
    )

    encoded_bytes = base64.b64encode(image.file.read())
    encoded_string = encoded_bytes.decode('utf-8')

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type=image.content_type,
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
                    """,
                ),
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
            yield chunk.text

    return StreamingResponse(generate_stream(), media_type="text/plain")
