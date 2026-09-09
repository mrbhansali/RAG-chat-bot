"""
Upload files, then chat with them.

Run: streamlit run app.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from config import GOOGLE_API_KEY, TOP_K
from src.ingestion import extract_text
from src.qa import answer_question
from src.transformation import chunk_text
from src.vector_store import build_vector_store

st.set_page_config(page_title="Chat with your files", page_icon="💬", layout="wide")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "file_names" not in st.session_state:
    st.session_state.file_names = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.title("💬 Chat with your files")
    st.caption("Upload PDFs, Word docs, or text files, then ask questions.")

    if not GOOGLE_API_KEY:
        st.warning("Set GOOGLE_API_KEY in your .env file before processing files.")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )

    if st.button("Process files", type="primary", disabled=not uploaded_files):
        all_chunks = []
        with st.spinner("Reading and indexing your files..."):
            for uploaded in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
                    tmp.write(uploaded.getvalue())
                    tmp_path = tmp.name

                text = extract_text(tmp_path)
                all_chunks.extend(chunk_text(text, source_name=uploaded.name))

            if not all_chunks:
                st.error("No extractable text found. If this is a scanned PDF, it needs OCR support first.")
            else:
                st.session_state.vectorstore = build_vector_store(all_chunks)
                st.session_state.file_names = [f.name for f in uploaded_files]
                st.session_state.chat_history = []
                st.success(f"Indexed {len(uploaded_files)} file(s) - {len(all_chunks)} chunks.")

    if st.session_state.file_names:
        st.info("Indexed: " + ", ".join(st.session_state.file_names))


st.header("Ask questions about your files")

if not st.session_state.vectorstore:
    st.info("Upload files and click 'Process files' in the sidebar to get started.")
else:
    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)

    query = st.chat_input("Ask something about your files...")
    if query:
        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, sources = answer_question(st.session_state.vectorstore, query, k=TOP_K)
            st.write(answer)

            with st.expander(f"Sources ({len(sources)})"):
                for doc in sources:
                    st.caption(doc.metadata.get("source", "unknown"))
                    st.text(doc.page_content[:400])

        st.session_state.chat_history.append((query, answer))
