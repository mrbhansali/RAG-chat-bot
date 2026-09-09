"""
Ingestion stage.

Extracts plain text from a file. Deliberately uses pure-Python
libraries only (pypdf, python-docx) so this runs anywhere pip works -
no poppler, tesseract, or libmagic required.

Trade-off: no OCR, so a scanned PDF (an image with no text layer)
will come back empty. Tables/images inside PDFs are not specially
handled - they just flow into the surrounding text as best pypdf can
manage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import docx  # python-docx
from pypdf import PdfReader


def extract_text(file_path: Union[str, Path]) -> str:
    """Dispatch to the right extractor based on file extension."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")

    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append(f"\n--- Page {i + 1} ---\n{text}")
    return "\n".join(pages)


def _extract_docx(path: Path) -> str:
    document = docx.Document(str(path))
    return "\n".join(p.text for p in document.paragraphs)
