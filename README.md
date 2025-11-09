# DILIX — Diligent Intelligent Assistant

DILIX is a **personal AI assistant** designed to help users interact with documents and answer questions using artificial intelligence. It provides a conversational interface, retrieves relevant knowledge from uploaded documents, and stores information in a vector database for context-aware responses. Think of it as a **Jarvis-like assistant for documents and knowledge management**.

---

## Features

- Conversational AI interface that responds intelligently to user queries
- Upload PDF and DOCX documents for context-aware answers
- Knowledge retrieval using a **vector database (Pinecone)** and embeddings
- Persistent chat history for seamless conversation

---

## Tech Stack / Tech Task

- **Frontend:** Streamlit — provides a clean, interactive chat interface  
- **Backend:** Python — handles conversation logic, memory management, and document processing  
- **Large Language Model:** **Groq LLM (e.g., LLaMA-based model)** — generates responses based on user queries and context  
- **Vector Database:** Pinecone — stores document embeddings for context-aware retrieval  
- **Document Processing:**  
  - PyMuPDF — extracts text from PDFs  
  - python-docx — extracts text from DOCX files  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Moulyadj-06/DILIX_Assistant.git
cd DILIX_Assistant


**Environment Variables / API Keys** (stored in `.env`):

```text
GROQ_API_KEY            # Your API key for accessing the Groq LLM
OPENAI_API_KEY           # Your OpenAI API key (optional for fallback tasks)
PINECONE_API_KEY         # API key for Pinecone vector database
PINECONE_ENV             # Pinecone environment (e.g., us-east-1)
PINECONE_INDEX_NAME      # Name of the Pinecone index (e.g., dilix-memory)
PINECONE_HOST            # Host URL of the Pinecone index
