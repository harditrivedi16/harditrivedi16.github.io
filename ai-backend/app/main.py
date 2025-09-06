# app/main.py (snippet)

from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.parser_pdf import extract_text_from_bytes, is_scanned

app = FastAPI()

@app.post("/parse_resume_text")
async def parse_resume_text(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf"}:
        raise HTTPException(status_code=400, detail="Please upload a PDF.")

    pdf_bytes = await file.read()
    pdf_text = extract_text_from_bytes(pdf_bytes)

    if is_scanned(pdf_text):
        # No selectable text found; later you can add OCR (e.g., Tesseract) if needed.
        return {"raw_text": "", "pages": [], "note": "No extractable text found; PDF appears scanned."}

    return {"raw_text": pdf_text.text, "pages": pdf_text.pages}
