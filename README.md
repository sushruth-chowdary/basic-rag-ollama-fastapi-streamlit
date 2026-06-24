# Local RAG PDF Chatbot using Ollama, ChromaDB, FastAPI, and Streamlit

A local Retrieval-Augmented Generation application that allows users to upload PDF documents, build a local knowledge base, and ask questions based on the uploaded content.

The project uses Ollama for local LLM responses, `nomic-embed-text` for local embeddings, ChromaDB for vector storage, FastAPI for backend APIs, and Streamlit for the user interface.

## Project Overview

This project was built to understand and implement the core RAG workflow manually.

It covers:

* PDF text extraction
* Text chunking
* Embedding generation
* Vector database storage
* Semantic search
* Prompt construction
* Source-backed answer generation
* FastAPI backend development
* Streamlit frontend development

## Tech Stack

* Python
* FastAPI
* Streamlit
* Ollama
* Llama 3.2
* nomic-embed-text
* ChromaDB
* LangChain
* PyPDF
* Pydantic

## Features

* Upload PDF documents through FastAPI or Streamlit
* Extract text from PDF pages using PyPDF
* Split documents into smaller chunks
* Generate local embeddings using Ollama `nomic-embed-text`
* Store document chunks and embeddings in ChromaDB
* Build a local document knowledge base
* Ask questions from uploaded PDFs
* Retrieve relevant document chunks using semantic similarity search
* Generate answers using Ollama `llama3.2`
* Display source-backed answers with page number and text preview
* List uploaded documents
* Reset the knowledge base
* Local-first design with no external LLM API dependency

## Knowledge Base

The knowledge base is created from uploaded PDF documents.

When a user uploads a PDF, the application extracts text from each page, splits the text into smaller chunks, converts those chunks into embeddings, and stores them in ChromaDB.

## Knowledge Base Flow

```text
PDF Upload
    ↓
PDF text extraction using PyPDF
    ↓
Text split into chunks
    ↓
Embedding generation using Ollama nomic-embed-text
    ↓
Chunks and embeddings stored in ChromaDB
    ↓
User asks a question
    ↓
Relevant chunks retrieved using similarity search
    ↓
Retrieved context sent to Ollama llama3.2
    ↓
Answer generated with source references
```

## What is Stored in the Knowledge Base?

For each uploaded PDF, the application stores:

* Text chunks
* Embedding vectors
* Source file path
* File name metadata
* Page number
* Text preview for source display

## Local Knowledge Base Storage

The vector knowledge base is stored locally in:

```text
chroma_db/
```

This folder is automatically generated when PDFs are uploaded and ingested.

## Uploaded PDF Storage

Uploaded PDFs are stored locally in:

```text
Data/
```

The `Data/` folder is excluded from GitHub because uploaded PDFs may contain private, copyrighted, or sensitive information.

## Why `chroma_db/` is Not Pushed to GitHub

The `chroma_db/` folder contains generated vector database files. These files are machine-specific and can be recreated by uploading PDFs again.

For this reason, `chroma_db/` is excluded from GitHub using `.gitignore`.

## Current Knowledge Base Behavior

* One PDF can be uploaded per `/upload` request.
* Multiple PDFs can still be added to the knowledge base by uploading them one after another.
* New uploads are added to the existing ChromaDB collection.
* The `/ask` endpoint searches across the stored knowledge base.
* The `/reset` endpoint clears uploaded PDFs and ChromaDB vector data.
* The knowledge base is local to the machine where the app is running.

## Project Architecture

```text
Streamlit UI
    ↓
FastAPI Backend
    ↓
PDF Processing
    ↓
Text Chunking
    ↓
Ollama Embeddings
    ↓
ChromaDB Vector Store
    ↓
Similarity Search
    ↓
Ollama LLM
    ↓
Answer with Sources
```

## API Endpoints

| Method | Endpoint     | Description                                           |
| ------ | ------------ | ----------------------------------------------------- |
| GET    | `/health`    | Checks API health status                              |
| POST   | `/upload`    | Uploads and ingests a PDF document                    |
| POST   | `/ask`       | Answers questions using the uploaded document context |
| GET    | `/documents` | Lists uploaded PDF documents                          |
| DELETE | `/reset`     | Clears uploaded PDFs and resets the knowledge base    |

## Project Structure

```text
BASIC_RAG/
│
├── Data/                 # Local uploaded PDFs, ignored by Git
├── chroma_db/            # Local ChromaDB vector database, ignored by Git
├── ingest.py             # Manual PDF ingestion script
├── query.py              # Terminal-based question answering script
├── main.py               # FastAPI backend
├── streamlit_UI.py       # Streamlit frontend
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── CHANGELOG.md          # Version history
├── VERSION               # Current project version
└── .gitignore            # Files and folders excluded from Git
```

## Prerequisites

Before running this project, install:

* Python 3.10 or higher
* Git
* Ollama

Also make sure Ollama is running locally.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sushruth-chowdary/basic-rag-ollama-fastapi-streamlit.git
cd basic-rag-ollama-fastapi-streamlit
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Pull Ollama Models

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 6. Run the FastAPI Backend

```powershell
python -m uvicorn main:app --reload
```

FastAPI Swagger documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

### 7. Run the Streamlit Frontend

Open a second terminal, activate the virtual environment again, and run:

```powershell
streamlit run streamlit_UI.py
```

## Usage

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Upload a PDF document.
4. Wait for the document to be processed and added to the knowledge base.
5. Ask a question related to the uploaded PDF.
6. View the answer and source preview.
7. Upload additional PDFs if needed.
8. Use reset to clear the local knowledge base.

## Example Questions

```text
What is ISO 27001?
```

```text
What is the purpose of this document?
```

```text
What are the main requirements mentioned in the document?
```

## Example API Request

### Ask Question

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is ISO 27001?\"}"
```

### Example Response

```json
{
  "question": "What is ISO 27001?",
  "answer": "ISO 27001 is an international standard for information security management systems.",
  "sources": [
    {
      "source": "C:\\Users\\sushr\\BASIC_RAG\\Data\\sample.pdf",
      "page": 1,
      "preview": "Information security management systems..."
    }
  ]
}
```

## Important Configuration Note

The current code uses local Windows paths:

```python
CHROMA_DB_DIR = "C:\\Users\\sushr\\BASIC_RAG\\chroma_db"
UPLOAD_DIR = "C:\\Users\\sushr\\BASIC_RAG\\Data"
```

If another user clones this project, they may need to update these paths in `main.py`, `ingest.py`, and `query.py` based on their local project location.

A future improvement would be to move these paths into a `.env` file or a configuration file.

## Version

Current version:

```text
0.1.0
```

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

## Git Ignore Policy

The following files and folders are excluded from GitHub:

```text
.venv/
__pycache__/
*.pyc
Data/
*.pdf
chroma_db/
ChromaDB/
.env
```

This keeps the repository clean and prevents local environments, uploaded PDFs, and generated vector database files from being pushed to GitHub.

## Current Limitations

* The upload endpoint currently accepts one PDF per request.
* Multiple PDFs can be added by uploading them one at a time.
* The project currently uses local hardcoded Windows paths.
* The app does not yet support user authentication.
* The app does not yet support cloud deployment.
* The app does not yet support advanced document filtering by file name.

## Future Improvements

* Support uploading multiple PDFs in a single request
* Move local paths to environment variables
* Add document-level filtering
* Add delete option for individual documents
* Add conversation history
* Add Docker support
* Add deployment instructions
* Add better error handling and logging
* Add support for DOCX and TXT files

## Notes

* This project runs fully locally using Ollama.
* No OpenAI API key is required.
* Uploaded documents are not pushed to GitHub.
* Vector database files are generated locally.
* This project is intended for learning and demonstrating the core RAG workflow.
