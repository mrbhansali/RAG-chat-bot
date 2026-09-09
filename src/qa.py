"""
Question-answering stage.

Retrieves relevant chunks for a question and asks the LLM to answer
using only that context, citing which file(s) it drew from.
"""

from __future__ import annotations

from typing import List, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI

from config import LLM_MODEL, LLM_TEMPERATURE, TOP_K
from src.vector_store import retrieve

_SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about the documents "
    "provided below. Only use the provided context to answer. If the "
    "context doesn't contain enough information, say so clearly instead "
    "of guessing."
)


def _build_prompt(chunks: List[Document], query: str) -> str:
    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}" for doc in chunks
    )
    return f"{_SYSTEM_PROMPT}\n\nCONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"


def answer_question(vectorstore: Chroma, query: str, k: int = TOP_K) -> Tuple[str, List[Document]]:
    """Retrieve context for `query` and return (answer, chunks_used)."""
    chunks = retrieve(vectorstore, query, k=k)
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    response = llm.invoke(_build_prompt(chunks, query))
    return response.content, chunks
