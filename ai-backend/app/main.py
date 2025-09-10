from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.parser_pdf import extract_text_from_bytes, is_scanned
from app.services.ai import extract_user_data
import logging
import traceback

app = FastAPI()

# Configure logging for Spaces (stdout)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Allow frontend(s) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://harditrivedi16.github.io",  # GitHub Pages
        "https://*.hf.space",                # Hugging Face Spaces
        "http://localhost:3000",             # local React dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health_check():
    """Kubernetes/Spaces style health probe"""
    return {"status": "ok"}

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    logging.info(" [DEBUG] /ping called")
    return {"message": "pong"}

@app.post("/extract")
async def extract_resume(file: UploadFile = File(...)):
    """Extract resume text and structured user data"""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    pdf_text = extract_text_from_bytes(pdf_bytes)

    if is_scanned(pdf_text):
        return {
            "schema_version": "v1.0",
            "userData": {},
            "warnings": [],
            "errors": ["No extractable text found — resume appears to be scanned."],
        }

    try:
        user_data_dict, warnings = extract_user_data(pdf_text.text)
        return {
            "schema_version": "v1.0",
            "userData": user_data_dict,
            "warnings": warnings,
            "errors": [],
        }
    except Exception as e:
        logging.exception("Extraction failed")
        # Safer: don’t expose full traceback in prod, only in debug
        return {
            "schema_version": "v1.0",
            "userData": {},
            "warnings": [],
            "errors": [f"Extraction failed: {type(e).__name__}: {str(e)}"],
            # comment this out in prod if too verbose:
            "debug": traceback.format_exc(),
        }
