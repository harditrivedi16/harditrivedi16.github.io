import re
import json
from typing import List, Tuple, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_huggingface import HuggingFaceEndpoint  # ✅ use this one only

from app.config import HF_API_TOKEN, HF_LLM_REPO
from app.models import (
    UserData, SocialIcon, ExperienceEntry, EducationEntry,
    ProjectDescriptions, ProjectDates
)
from app.services.rag import index_resume, retrieve

import os
from dotenv import load_dotenv



load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_LLM_REPO = os.getenv("HF_LLM_REPO")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
RAG_CHUNK_LEN = int(os.getenv("RAG_CHUNK_LEN", "800"))


# ---------- LLM ----------
load_dotenv()

# Hugging Face Space will inject secrets at runtime
HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_LLM_REPO = os.getenv("HF_LLM_REPO", "meta-llama/Meta-Llama-3-8B-Instruct")

# Configure LLM (Inference API)
llm = HuggingFaceEndpoint(
    repo_id=HF_LLM_REPO,
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,
    huggingfacehub_api_token=HF_API_TOKEN,
)

# ---------- Prompts ----------
_extract_prompt = ChatPromptTemplate.from_template(
    """
You extract resume data as STRICT JSON for this schema:

{{
  "firstName": string|null,
  "lastName": string|null,
  "headline": string|null,

  "icons": [{{"image": string, "url": string, "handle": string}}],

  "instaLink": string|null,
  "instagramId": string|null,
  "instaQuerry": string|null,

  "myDescription": [string],  // one string ~200 words

  "githubId": string|null,
  "repos": [string],

  "projectDesc": {{ "<project>": [line1, line2], ... }},
  "projectDates": {{ "<project>": "YYYY" | "Mon YYYY" }},

  "experience": [
    {{
      "role": string, "company": string, "timeline": string, "location": string,
      "bullets": [string]
    }}
  ],
  "education": [
    {{
      "degree": string, "field": string|null, "university": string,
      "start": string|null, "end": string|null, "location": string|null,
      "details": [string], "courses": [string]
    }}
  ],
  "skills": [string]
}}

MANDATORY RULES:
- Return ONLY valid JSON for the exact schema above.
- Enumerate **ALL** entries present in the resume for experience, education, and projects (not just the most recent).
- If a value is unknown, use null or [].
- Headline: concise professional title from the resume.
- myDescription: a single paragraph (~200 words) inside an array with exactly one string.
- icons: include GitHub, LinkedIn, Twitter/X, Instagram, Facebook, Medium if present. For each, set:
  - "url": the full profile URL as found
  - "handle": just the username/slug (no extra path, no slashes)
- repos: extract ALL GitHub repository names from links (just the repo name after the last "/"; do not include the owner). Dedupe.
- projectDesc/projectDates:
  - Create an entry for **every** project you can identify (from project sections, bullets, repo names, or links).
  - Each description must be exactly two lines, each ≤150 characters, informative and distinct.
  - Dates: choose the closest single year or "Mon YYYY" you can infer for each project. If absent, omit that key or set a best available year.
- experience: create an entry for all the roles. Keep "timeline" exactly as shown in the resume (e.g., "Jan 2023 – Aug 2024").
  - "bullets": use 2–6 concise impact bullets per role; quote faithfully from resume (light rewriting allowed for clarity).
- education: create an entry for all the degrees degrees. Include courses if explicitly listed; otherwise leave [].
- skills: include all unique skills; dedupe; prefer canonical names (e.g., "PyTorch" not "Pytorch").


RESUME TEXT:
{resume_text}

Return ONLY JSON:
"""
)

_rag_desc_prompt = ChatPromptTemplate.from_template(
    """
You write a single ~200-word professional summary based ONLY on provided context.

Context:
{context}

Return only the paragraph, no preface or notes.
"""
)

# ---------- Utilities ----------
def _json_only(s: str) -> dict:
    start, end = s.find("{"), s.rfind("}")
    blob = s[start:end+1] if start != -1 and end != -1 else "{}"
    try:
        return json.loads(blob)
    except Exception:
        return {}

def _username_from_url(url: str) -> str:
    try:
        # strip trailing slash and query; keep last path segment
        core = re.sub(r"[?#].*$", "", url.strip().rstrip("/"))
        handle = core.split("/")[-1]
        return handle or ""
    except Exception:
        return ""

def _normalize_icons(raw_icons: List[Dict]) -> List[SocialIcon]:
    # Map known providers to your icon set & base URLs
    catalog = {
        "github.com": ("fa-github", "https://github.com/"),
        "linkedin.com": ("fa-linkedin", "https://linkedin.com/in/"),
        "x.com": ("fa-twitter", "https://www.twitter.com/"),
        "twitter.com": ("fa-twitter", "https://www.twitter.com/"),
        "instagram.com": ("fa-instagram", "https://www.instagram.com/"),
        "facebook.com": ("fa-facebook", "https://www.facebook.com/"),
        "medium.com": ("fa-medium", "https://www.medium.com/"),
    }
    out: List[SocialIcon] = []
    for item in raw_icons or []:
        url = str(item.get("url", "")).strip()
        if not url:
            continue
        domain = ""
        m = re.search(r"https?://([^/]+)/", url + "/")
        if m: domain = m.group(1).lower()
        icon, base = None, None
        for d, (ic, baseurl) in catalog.items():
            if d in domain:
                icon, base = ic, baseurl
                break
        if not icon:
            # skip unknown providers to avoid breaking UI
            continue
        handle = item.get("handle") or _username_from_url(url.replace(base or "", ""))
        out.append(SocialIcon(id=len(out), image=icon, url=base or url, handle=handle, style="socialicons"))
    return out

def _backfill_github_from_icons(icons: List[SocialIcon]) -> str:
    for ic in icons:
        if ic.image == "fa-github" and ic.handle:
            return ic.handle
    return ""

# ---------- Public API ----------
def extract_user_data(resume_text: str, doc_id: str = "resume") -> Tuple[dict, List[str]]:
    """
    1) Index the resume remotely (Qdrant) so we can RAG when needed.
    2) One-pass LLM JSON extraction for schema fields.
    3) Optional RAG polish for the ~200-word myDescription.
    4) Normalize icons/handles/links to your frontend's expectations.
    """
    # Ensure resume is in vector store (remote; idempotent-ish)
    print("[DEBUG] Starting extract_user_data...")
    index_resume(doc_id, resume_text)
    print("[DEBUG] Indexed resume in vectorstore")

    # First pass extraction
    chain = _extract_prompt | _llm() | StrOutputParser() | RunnableLambda(_json_only)
    print("[DEBUG] Invoking chain...")
    data = chain.invoke({"resume_text": resume_text}) or {}
    print("[DEBUG] Chain completed")

    # Normalize icons
    icons = _normalize_icons(data.get("icons", []))

    # GitHub id from icons if missing
    github_id = data.get("githubId") or _backfill_github_from_icons(icons) or None

    # Optional: RAG-refine myDescription from retrieved chunks
    docs = retrieve(query="Produce a professional summary of the candidate.", k=4)
    ctx = "\n\n---\n\n".join(d.page_content for d in docs) if docs else resume_text
    desc_chain = _rag_desc_prompt | _llm() | StrOutputParser()
    refined_desc = desc_chain.invoke({"context": ctx}).strip()
    my_desc_list = [refined_desc] if refined_desc else (data.get("myDescription") or [])

    # Build strongly-typed model
    ud = UserData(
        firstName=data.get("firstName"),
        lastName=data.get("lastName"),
        headline=data.get("headline"),
        icons=[i.dict() for i in icons],  # Pydantic will re-validate

        instaLink=data.get("instaLink"),
        instagramId=data.get("instagramId"),
        instaQuerry=data.get("instaQuerry"),

        myDescription=my_desc_list,

        githubId=github_id,
        repos=data.get("repos") or [],

        projectDesc=ProjectDescriptions(__root__=data.get("projectDesc") or {}),
        projectDates=ProjectDates(__root__=data.get("projectDates") or {}),

        experience=[
            ExperienceEntry(
                role=e.get("role",""),
                company=e.get("company",""),
                timeline=e.get("timeline",""),
                location=e.get("location",""),
                bullets=e.get("bullets") or []
            )
            for e in (data.get("experience") or [])
            if isinstance(e, dict)
        ],
        education=[
            EducationEntry(
                degree=ed.get("degree",""),
                field=ed.get("field"),
                university=ed.get("university",""),
                start=ed.get("start"),
                end=ed.get("end"),
                location=ed.get("location"),
                details=ed.get("details") or [],
                courses=ed.get("courses") or []
            )
            for ed in (data.get("education") or [])
            if isinstance(ed, dict)
        ],
        skills=data.get("skills") or [],
    )
    
    warnings = []
    if not ud.githubId:
        warnings.append("Missing GitHub ID")
    if not ud.skills:
        warnings.append("No skills detected")

    return ud.dict(), warnings

def make_user_data_js(resume_text: str, doc_id: str = "resume") -> str:
    """
    Convenience: run extraction and return JS string for frontend.
    You already have formatter.userdata_js_from_struct; call that if preferred.
    """
    from app.services.formatter import userdata_js_from_struct
    ud = extract_user_data(resume_text, doc_id=doc_id)
    return userdata_js_from_struct(ud)
