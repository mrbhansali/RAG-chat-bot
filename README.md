# Chat with your files

Upload PDFs / Word docs / text files, then ask questions about them.
No system dependencies (no poppler, tesseract, or libmagic) - everything
is pure Python, so `pip install` is the only setup step.

## Structure

```
.
├── app.py                 # Streamlit UI - upload + chat
├── config.py                # Model names, chunk size, API key handling
├── requirements.txt
├── .env.example
└── src/
    ├── ingestion.py          # PDF/DOCX/TXT -> plain text
    ├── transformation.py     # plain text -> overlapping chunks
    ├── vector_store.py        # embed chunks, similarity search (in-memory Chroma)
    └── qa.py                   # retrieve + generate answer
```

## Run it (3 steps)

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
# then open .env and paste in your key
```

Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (Google AI Studio's Gemini API has a free tier with rate limits).

```bash
streamlit run app.py
```

That's it — open the URL Streamlit prints (usually `http://localhost:8501`), upload a file, click **Process files**, and start chatting.

## Known limitations (trade-offs for simplicity)

- **No OCR.** A scanned PDF (an image with no text layer) will extract empty text. If you need this, we'd add `pytesseract` back in, which brings back the Tesseract system dependency.
- **Tables/images aren't specially parsed.** They just flow into the surrounding text as plain characters.
- **No persistence.** Each Streamlit session starts with an empty index — closing the tab loses it. Fine for demos; for production, `src/vector_store.py` is the one file to change (add a `persist_directory`, or swap Chroma for a hosted vector DB).

## Deploying

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo, point it at `app.py`.
3. In the app's **Secrets** panel, add:
   ```
   GOOGLE_API_KEY = "your-key-here"
   ```
4. Deploy. No `packages.txt` needed this time — there are no system dependencies.
