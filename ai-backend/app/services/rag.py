# app/services/rag.py
from __future__ import annotations

import os
import logging
from typing import List, Tuple, Optional

import spacy
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------
load_dotenv()  # local dev only; Spaces injects env vars automatically

EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "thenlper/gte-small")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ai-portfolio-db")

# defaults
RAG_CHUNK_LEN = int(os.getenv("RAG_CHUNK_LEN", "800"))
EMBED_DIM = 384  # for gte-small (adjust if you switch models)

# ---------------------------------------------------------
# Lazy singletons
# ---------------------------------------------------------
_nlp: Optional["spacy.language.Language"] = None
_emb: Optional[HuggingFaceEmbeddings] = None
_qc: Optional[QdrantClient] = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def _get_emb():
    global _emb
    if _emb is None:
        _emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return _emb

def get_qdrant_client():
    global _qc
    if _qc is None:
        _qc = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            timeout=30,
        )
        _ensure_collection(_qc)
    return _qc

def _ensure_collection(client: QdrantClient):
    """
    Create collection with known dim if missing.
    Safe to call repeatedly.
    """
    try:
        names = [c.name for c in client.get_collections().collections]
    except Exception:
        logging.exception("Failed to list Qdrant collections")
        raise

    if QDRANT_COLLECTION in names:
        return

    try:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )
    except Exception:
        logging.exception("create_collection failed (may already exist)")

# ---------------------------------------------------------
# Chunking
# ---------------------------------------------------------
def sentence_chunk(text: str, max_len: int = RAG_CHUNK_LEN) -> List[str]:
    """
    Sentence-aware chunking up to ~max_len chars per chunk.
    """
    doc = _get_nlp()(text or "")
    chunks, buf = [], ""
    for sent in doc.sents:
        cand = (buf + " " + sent.text).strip()
        if len(cand) > max_len and buf:
            chunks.append(buf.strip())
            buf = sent.text
        else:
            buf = cand
    if buf:
        chunks.append(buf.strip())

    return [c.replace("\u00A0", " ").strip() for c in chunks if c.strip()]

# ---------------------------------------------------------
# Public API
# ---------------------------------------------------------
def index_resume(doc_id: str, text: str) -> Qdrant:
    """
    Index a resume text into Qdrant vector store.
    """
    chunks = sentence_chunk(text) or ["."]
    metas = [{"source": f"{doc_id}#chunk{i}"} for i in range(len(chunks))]

    client = get_qdrant_client()
    vs = Qdrant.from_texts(
        texts=chunks,
        embedding=_get_emb(),
        metadatas=metas,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=QDRANT_COLLECTION,
    )
    return vs

def get_vectorstore() -> Qdrant:
    """
    Return Qdrant vectorstore wrapper.
    """
    return Qdrant(
        client=get_qdrant_client(),
        collection_name=QDRANT_COLLECTION,
        embeddings=_get_emb(),
    )

def build_or_get_vs(doc_id: str, text: str) -> Tuple[Qdrant, List[str]]:
    """
    For a fresh document, (re)index and return (vectorstore, chunks).
    """
    vs = index_resume(doc_id or "resume", text)
    return vs, sentence_chunk(text)

def retrieve(query: str, k: int = 4):
    """
    Retrieve top-k similar chunks for the query.
    """
    return get_vectorstore().similarity_search(query, k=k)
