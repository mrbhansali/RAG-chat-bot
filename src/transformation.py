"""
Transformation stage.

Splits raw extracted text into overlapping chunks sized for embedding.
Much simpler than the original notebook's title-based chunking - no
document structure analysis, just a sliding window that tries to
break on paragraph/sentence boundaries where possible.
"""

from __future__ import annotations

from typing import Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_text(text: str, source_name: str) -> List[Dict[str, str]]:
    """Return a list of {"text": ..., "source": ...} chunks for one document."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    pieces = splitter.split_text(text)
    return [{"text": piece, "source": source_name} for piece in pieces if piece.strip()]
