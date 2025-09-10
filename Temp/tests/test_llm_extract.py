import os
import json
from app.services.parser_pdf import extract_text_from_bytes
from app.services.ai import extract_user_data

CURRENT_DIR = os.path.dirname(__file__)
PDF_PATH = os.path.join(CURRENT_DIR, "Hardi_Resume.pdf")

if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"Hardi_Resume.pdf not found at: {PDF_PATH}")

with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

print("Extracting text from PDF...")
pdf_text = extract_text_from_bytes(pdf_bytes)
resume_text = pdf_text.text

print("Invoking LLM extraction...")
user_data_dict, warnings = extract_user_data(resume_text, doc_id="test_resume")

print("\nExtracted Fields:")
print(f"Name: {user_data_dict.get('firstName')} {user_data_dict.get('lastName')}")
print(f"Headline: {user_data_dict.get('headline')}")
print(f"GitHub ID: {user_data_dict.get('githubId')}")
print(f"Skills: {', '.join(user_data_dict.get('skills', []))}")
print(f"Experience count: {len(user_data_dict.get('experience', []))}")
print(f"Education count: {len(user_data_dict.get('education', []))}")
print(f"My Description:\n{user_data_dict.get('myDescription', [''])[0]}")

if warnings:
    print("\n Warnings:")
    for w in warnings:
        print(f"- {w}")
