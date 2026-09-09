"""
Minimal configuration. Only one API key is needed (Google AI Studio / Gemini,
which has a free tier). Values can be overridden via .env or Streamlit secrets.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _secret(key: str, default: Optional[str] = None) -> Optional[str]:
    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


GOOGLE_API_KEY = _secret("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ.setdefault("GOOGLE_API_KEY", GOOGLE_API_KEY)

LLM_MODEL = _secret("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = _secret("EMBEDDING_MODEL", "models/gemini-embedding-001")
LLM_TEMPERATURE = float(_secret("LLM_TEMPERATURE", "0"))

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4
