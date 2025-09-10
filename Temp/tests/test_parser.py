# tests/test_parser.py

import os
from app.services.parser_pdf import extract_text_from_bytes, is_scanned

# Correctly locate the PDF file relative to this script
CURRENT_DIR = os.path.dirname(__file__)
PDF_PATH = os.path.join(CURRENT_DIR, "Hardi_Resume.pdf")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"sample_resume.pdf not found at: {PDF_PATH}")

# Read and parse the PDF
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

pdf_text = extract_text_from_bytes(pdf_bytes)

# Check if it's scanned or parseable
if is_scanned(pdf_text):
    print("PDF appears to be scanned (image-based). No extractable text.")
else:
    print("Extracted text:")
    print(pdf_text.text[:500])  # Preview first 500 characters
