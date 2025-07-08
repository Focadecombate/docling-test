import logging
from io import BytesIO
from uuid import uuid4

from docling_core.types.io import DocumentStream
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from .ai_parsing.lang import convert_markdown_to_json_langchain_streaming
from .ai_parsing.model import Fatura
from .conversions.parse_expense import pdf_to_markdown
from .otel import setup_otel

logging.basicConfig(level=logging.INFO)
setup_otel()

app = FastAPI()


class Response(BaseModel):
    result: Fatura


@app.post("/")
async def parse_document(file: UploadFile):
    file_name = file.filename if file.filename else f"document-{uuid4()}.pdf"

    markdown_content = pdf_to_markdown(
        DocumentStream(
            name=file_name,
            stream=BytesIO(await file.read()),
        )
    )

    try:
        result = convert_markdown_to_json_langchain_streaming(markdown_content)
    except Exception as e:
        logging.error(f"Error during parsing: {e}")
        raise HTTPException(status_code=500, detail="Error during parsing")

    return Response(result=result)
