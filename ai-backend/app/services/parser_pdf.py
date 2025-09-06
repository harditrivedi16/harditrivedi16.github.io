# app/services/parser_pdf.py
from __future__ import annotations

import io
import re
from typing import List, Tuple, Optional

import pdfplumber
from PyPDF2 import PdfReader


class PDFText:
    """
    Container for extracted text.
    """
    def __init__(self, pages: List[str]):
        self.pages = pages                      # page-wise text (already cleaned)
        self.text = "\n\n".join(pages).strip()  # full document text


def _clean(s: Optional[str]) -> str:
    """
    Normalize whitespace and strip noisy spaces.
    """
    if not s:
        return ""
    s = s.replace("\x00", " ")          # null bytes → spaces
    s = re.sub(r"[ \t]+", " ", s)       # collapse runs of spaces/tabs
    s = re.sub(r"[ \t]*\n[ \t]*", "\n", s)  # trim spaces around newlines
    s = re.sub(r"\n{3,}", "\n\n", s)    # cap blank lines to 2
    return s.strip()


def _extract_with_pdfplumber(file_like: io.BytesIO) -> List[str]:
    pages: List[str] = []
    file_like.seek(0)
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            pages.append(_clean(txt))
    return pages


def _extract_with_pypdf2(file_like: io.BytesIO) -> List[str]:
    pages: List[str] = []
    file_like.seek(0)
    reader = PdfReader(file_like)
    for p in reader.pages:
        txt = p.extract_text() or ""
        pages.append(_clean(txt))
    return pages


def extract_text_from_bytes(pdf_bytes: bytes) -> PDFText:
    """
    Main entry: pass raw PDF bytes (e.g., from FastAPI UploadFile).
    Tries pdfplumber, falls back to PyPDF2.
    """
    bio = io.BytesIO(pdf_bytes)

    # Try pdfplumber
    try:
        pages = _extract_with_pdfplumber(bio)
    except Exception:
        pages = []

    # Fallback if plumber failed or yielded no text (likely scanned PDF)
    if not any(pages):
        try:
            pages = _extract_with_pypdf2(bio)
        except Exception:
            pages = []

    return PDFText(pages=pages)


def extract_text_from_path(path: str) -> PDFText:
    """
    Convenience helper if you have a file path instead of bytes.
    """
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    return extract_text_from_bytes(pdf_bytes)


def is_scanned(pdf_text: PDFText) -> bool:
    """
    Heuristic: no extractable text ⇒ likely scanned/needs OCR.
    """
    return len(pdf_text.text.strip()) == 0
