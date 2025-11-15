# DILIX — Diligent Intelligent Assistant

DILIX is a personal AI assistant designed to help users interact with documents, organize files, and answer questions using artificial intelligence. It provides a natural conversational interface, retrieves relevant knowledge from uploaded documents, and stores information in a vector database for intelligent, context-aware responses. Along with document understanding, DILIX includes an automated file management system that categorizes, renames, and organizes files effortlessly.

Think of it as a Jarvis-like assistant for documents, knowledge management, and smart file organization.**.

---

## Features

- Conversational Interface: Responds naturally to queries and provides context-aware answers.
- Document Processing: Extracts text, summaries, and insights from PDFs, Word files, text documents, and images.
- Vector Database Integration: Stores document embeddings for fast and accurate semantic retrieval.
- Knowledge Retrieval: Answers questions by finding relevant information across all uploaded documents.
- Intelligent File Organizer: Automatically manages and structures your files using AI.

---

## Workflow

- User uploads file
- DILIX extracts text + metadata
- Embeddings generated and stored
- File organized into correct folder
- User asks a question
- Relevant chunks retrieved + answer generated

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
