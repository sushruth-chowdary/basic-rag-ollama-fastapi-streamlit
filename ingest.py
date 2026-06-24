import os
import sys
import shutil
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
# Contains the path for Chroma DB directory
CHROMA_DB_DIR = "C:\\Users\\sushr\\BASIC_RAG\\chroma_db"
COLLECTION_NAME = "BasicRAG"
# Vector Embeddings Model
EMBEDDINGS_MODEL = "nomic-embed-text"
# Function to load PDFs from a directory
def load_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"PDF file {pdf_path} does not exist.")
        return None
    reader = PdfReader(pdf_path)
    documents = []
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            document = Document(
                page_content=page_text,
                metadata={
                    "source": pdf_path,
                    "page": page_number
                }
            )
            documents.append(document)
    print(f"Loaded PDF: {pdf_path}")
    print(f"Total pages loaded: {len(documents)}")
    return documents
# Function to split documents into smaller chunks
def split_documents(documents):
    # Splits PDF into smaller chunks. Smaller chunks are easier to process and store.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks
# Function to create vector embeddings for the text chunks
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
        print(f"Deleted old Chroma DB: {CHROMA_DB_DIR}")


def main() :
    # Usage must be in the format of : python ingest.py <path_to_pdf_directory>
    if len(sys.argv) < 2:
        print("Please provide a valid path.")
        print("Example: python ingest.py /path/to/pdf/directory")
        return 
    pdf_directory = sys.argv[1]
    delete_old_chroma_db()
    documents = load_pdf(pdf_directory)
    if documents is None:
        return
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    main()