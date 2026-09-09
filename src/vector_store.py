"""
Vector store stage.

Uses Chroma in ephemeral, in-memory mode (no persist_directory) - each
session gets a fresh vector store, nothing is written to disk. That
keeps the app stateless and avoids any file-path/permission issues,
which is exactly what a "just run it" app wants. Swap this for a
persisted or hosted vector DB later if you need documents to survive
a restart.
"""

from __future__ import annotations

from typing import Dict, List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import EMBEDDING_MODEL, TOP_K


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)


def build_vector_store(chunks: List[Dict[str, str]]) -> Chroma:
    """Embed a list of {"text", "source"} chunks into a fresh in-memory Chroma store."""
    documents = [
        Document(page_content=chunk["text"], metadata={"source": chunk["source"]}) for chunk in chunks
    ]
    return Chroma.from_documents(documents=documents, embedding=_embeddings())


def retrieve(vectorstore: Chroma, query: str, k: int = TOP_K) -> List[Document]:
    """Similarity search for the k most relevant chunks."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)
