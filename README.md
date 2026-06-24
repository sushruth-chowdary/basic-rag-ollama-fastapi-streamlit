# Local RAG PDF Chatbot using Ollama, ChromaDB, FastAPI, and Streamlit

A local Retrieval-Augmented Generation application that allows users to upload PDF documents and ask questions based on the uploaded content. The application uses Ollama for local LLM responses, ChromaDB for vector storage, FastAPI for backend APIs, and Streamlit for the user interface.

## Project Overview

This project was built to understand and implement the core RAG workflow manually. It covers PDF text extraction, text chunking, embedding generation, vector database storage, semantic retrieval, prompt construction, and source-backed answer generation.

## Tech Stack

* Python
* Ollama
* Llama 3.2
* nomic-embed-text
* ChromaDB
* FastAPI
* Streamlit
* LangChain
* PyPDF

## Features

* Upload PDF documents
* Extract text from PDF pages
* Split documents into smaller chunks
* Generate local embeddings using Ollama
* Store embeddings in ChromaDB
* Retrieve relevant document chunks using semantic search
* Generate answers using a local Ollama LLM
* Display source previews with file name and page number
* FastAPI backend with REST endpoints
* Streamlit frontend for user interaction

## Project Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation using Ollama
    ↓
Vector Storage in ChromaDB
    ↓
User Question
    ↓
Similarity Search
    ↓
Context + Question sent to LLM
    ↓
Answer with Sources
```

## API Endpoints

| Method | Endpoint  | Description                                       |
| ------ | --------- | ------------------------------------------------- |
| GET    | `/health` | Checks API health status                          |
| POST   | `/upload` | Uploads and ingests PDF documents                 |
| POST   | `/ask`    | Answers questions using uploaded document context |

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sushruth-chowdary/basic-rag-ollama-fastapi-streamlit.git
cd basic-rag-ollama-fastapi-streamlit
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install and pull Ollama models

Make sure Ollama is installed on your system, then pull the required models:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Run the FastAPI backend

```powershell
python -m uvicorn main:app --reload
```

FastAPI Swagger docs will be available at:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the Streamlit frontend

Open a second terminal and run:

```powershell
streamlit run streamlit_UI.py
```

## Usage

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Upload one or more PDF files.
4. Ask questions based on the uploaded documents.
5. View the generated answer along with source previews.

## Version

Current version: `0.1.0`

## Version Control

This project uses Git for version control.

Version format:

```text
MAJOR.MINOR.PATCH
```

Current release:

```text
v0.1.0 - Initial working local RAG release
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Notes

* This project runs locally using Ollama.
* Uploaded PDFs are excluded from GitHub using `.gitignore`.
* ChromaDB vector data is excluded from GitHub because it is generated locally.
* The project is intended for learning and demonstrating a basic RAG workflow.
