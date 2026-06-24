from pydantic import BaseModel
from fastapi import FastAPI
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
import os
import shutil 
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
CHROMA_DB_DIR = "C:\\Users\\sushr\\BASIC_RAG\\chroma_db"
COLLECTION_NAME = "BasicRAG"
EMBEDDINGS_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
UPLOAD_DIR = "C:\\Users\\sushr\\BASIC_RAG\\Data"
app = FastAPI(
    title = "Basic RAG API",
    description = "A simple RAG API using Ollama and Chroma",
    version = "0.1.0"
)
def load_pdf(file_path):
    reader = PdfReader(file_path)
    documents = []
    file_name = os.path.basename(file_path)
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text: 
            document = Document(
                page_content = page_text,
                metadata = {
                    "source": file_path,
                    "file_name" : file_name,
                    "page": page_number,
                }
            )
            documents.append(document)
    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    return text_splitter.split_documents(documents)

# def create_vector_store(chunks):
#     embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)
#     vector_store = Chroma.from_documents(
#         embedding = embeddings,
#         collection_name=COLLECTION_NAME,
#         persist_directory = CHROMA_DB_DIR
#     )
#     vector_store.add_documents(documents=chunks)
#     return vector_store
def create_vector_store(chunks):
    embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    vector_store.add_documents(chunks)

    return vector_store

def delete_old_chroma_db():
    if os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)

class QuestionRequest(BaseModel):
    question: str

def load_vector_store():
    embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)
    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )
    return vector_store

def retrieve_context(vector_store, question):
    relevant_docs = vector_store.similarity_search(
        query=question,
        k=3
    )
    return relevant_docs
def generate_response(relevant_docs, question):
    llm = ChatOllama(model=LLM_MODEL)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    prompt = f"""
You are a helpful AI assistant.

Answer the question using only the context below.

Rules:
1. Do not use outside knowledge.
2. If the answer is not found in the context, say:
"I could not find the answer in the provided document."
3. Keep the answer simple and clear.

Context:
{context}

Question:
{question}

Answer: 
"""
    response = llm.invoke(prompt)
    return response.content

@app.get("/health")
def health_check():
    return {
        "status" : "healthy",
        "message" : "RAG API is running successfully."
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    vector_store = load_vector_store()
    relevant_docs = retrieve_context(vector_store, request.question)
    if not relevant_docs:
        return {
            "answer": "I could not find the answer in the provided document.",
            "sources": []
        }
    response = generate_response(relevant_docs, request.question)
    sources = []
    for doc in relevant_docs:
        sources.append({
            "source" : doc.metadata.get("source", "Unknown source"),
            "page" : doc.metadata.get("page", "Unknown page"),
            "preview" : doc.page_content[:300]
        })
    return {
        "question" : request.question,
        "answer" : response,
        "sources" : sources
    }
    sources.append({
    "file_name": doc.metadata.get("file_name", "Unknown file"),
    "source": doc.metadata.get("source", "Unknown source"),
    "page": doc.metadata.get("page", "Unknown page"),
    "preview": doc.page_content[:300]
})


# @app.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(".pdf"):
#         return {
#             "message": "Only PDF files are supported."
#         }

#     os.makedirs(UPLOAD_DIR, exist_ok=True)

#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())


#     documents = load_pdf(file_path)

#     if not documents:
#         return {
#             "message": "No readable text found in the PDF."
#         }

#     chunks = split_documents(documents)

#     create_vector_store(chunks)

#     return {
#         "message": "PDF uploaded and ingested successfully.",
#         "file_name": file.filename,
#         "pages_loaded": len(documents),
#         "chunks_created": len(chunks)
#     }
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "message": "Only PDF files are supported."
        }

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    documents = load_pdf(file_path)

    if not documents:
        return {
            "message": "No readable text found in the PDF."
        }

    chunks = split_documents(documents)

    create_vector_store(chunks)

    return {
        "message": "PDF uploaded and added to knowledge base successfully.",
        "file_name": file.filename,
        "pages_loaded": len(documents),
        "chunks_created": len(chunks)
    }

@app.get("/documents")
def list_documents():
    if not os.path.exists(UPLOAD_DIR):
        return {
            "documents": []
        }

    files = [
        file_name
        for file_name in os.listdir(UPLOAD_DIR)
        if file_name.lower().endswith(".pdf")
    ]

    return {
        "documents": files,
        "count": len(files)
    }

@app.delete("/reset")
def reset_knowledge_base():
    if os.path.exists(CHROMA_DB_DIR):
        shutil.rmtree(CHROMA_DB_DIR)

    if os.path.exists(UPLOAD_DIR):
        for file_name in os.listdir(UPLOAD_DIR):
            if file_name.lower().endswith(".pdf"):
                file_path = os.path.join(UPLOAD_DIR, file_name)
                os.remove(file_path)

    return {
        "message": "Knowledge base reset successfully."
    }