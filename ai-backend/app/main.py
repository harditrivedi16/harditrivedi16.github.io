# app/main.py (snippet)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.formatter import to_frontend_userdata, from_frontend_userdata
from typing import Dict, Any

from app.services.parser_pdf import extract_text_from_bytes, is_scanned
from app.services.formatter import to_frontend_userdata
from app.models import UserData

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://harditrivedi16.github.io", "http://localhost:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
@app.post("/parse_resume_text")
async def parse_resume_text(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf"}:
        raise HTTPException(status_code=400, detail="Please upload a PDF.")

    pdf_bytes = await file.read()
    pdf_text = extract_text_from_bytes(pdf_bytes)

    if is_scanned(pdf_text):
       
        return {"raw_text": "", "pages": [], "note": "No extractable text found; PDF appears scanned."}

    return {"raw_text": pdf_text.text, "pages": pdf_text.pages}

@app.post("/regenerate")
async def regenerate(payload: Dict[str, Any]):
    """
    Accepts:
      { "userData": <frontend-shape>, "resumeText": "<optional>" }
    We will: convert inbound to normalized -> fill missing (AI later) -> format back.
    """
    incoming = payload.get("userData") or {}
    resume_text = payload.get("resumeText", "")

    
    normalized = from_frontend_userdata(incoming)
    if resume_text:
        normalized.raw_resume_text = resume_text

 
    return to_frontend_userdata(normalized)
