# 🤖 Advanced Hybrid RAG Engine

A professional-grade Retrieval-Augmented Generation (RAG) system that allows users to "chat" with their documents (PDF, JSON, TXT) using the power of **Llama 3.3** and **Groq**.

## 🚀 Key Features
* **Hybrid Search:** Combines semantic meaning with keyword matching for high accuracy.
* **Persistent Memory:** Uses **FAISS** to save document embeddings locally to disk.
* **Source Tracing:** Automatically identifies the filename and page number for every answer.
* **FastAPI Backend:** Industry-standard asynchronous API for high-speed processing.
* **Streamlit Frontend:** A clean, user-friendly chat interface with history.

## 🛠️ Tech Stack
* **LLM:** Llama-3.3-70b (via Groq Cloud)
* **Orchestration:** LangChain & LangChain-Classic
* **Vector Store:** FAISS (Facebook AI Similarity Search)
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
* **API Framework:** FastAPI
* **UI Framework:** Streamlit

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Hybrid-Search-RAG-Engine.git](https://github.com/YOUR_USERNAME/Hybrid-Search-RAG-Engine.git)
   cd Hybrid-Search-RAG-Engine