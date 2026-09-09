
# RAG Chatbot

Welcome! I built this **RAG (Retrieval-Augmented Generation) Chatbot** to demonstrate how we can leverage Large Language Models to securely and accurately interact with custom datasets. Instead of relying solely on an LLM's pre-trained memory, this application retrieves relevant information from a provided knowledge base to generate context-aware, reduced-hallucination answers.

## Live Demo
Check out the deployed application here: **[myrag-chat-bot.streamlit.app](https://myrag-chat-bot.streamlit.app/)**

## Key Features
* **Custom Knowledge Retrieval:** Users can query specific information, and the bot responds using only the provided context.
* **Interactive UI:** I built a clean, conversational, and responsive front-end using Streamlit.
* **Context-Aware Responses:** Leverages the RAG pipeline to ensure accuracy and cite specific data sources.
* **Fast Vector Search:** Optimized document chunking and embeddings for rapid information retrieval.

## Tech Stack
Here are the core technologies I used to build this project:
* **Frontend:** Streamlit
* **LLM Framework:** LangChain / LlamaIndex 
* **Embeddings & LLM:** OpenAI / HuggingFace 
* **Vector Database:** ChromaDB / FAISS / Pinecone 

## Running it Locally

If you want to clone this repository and test the app on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/mrbhansali/RAG-chat-bot.git](https://github.com/mrbhansali/RAG-chat-bot.git)
cd RAG-chat-bot

```

### 2. Install dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt

```

### 3. Set up Environment Variables

Create a `.env` file in the root directory and add your necessary API keys (e.g., for OpenAI):

```env
OPENAI_API_KEY=your_api_key_here

```

### 4. Run the application

```bash
streamlit run app.py

```
