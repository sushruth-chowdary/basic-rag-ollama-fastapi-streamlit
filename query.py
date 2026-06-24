import sys 
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma 

CHROMA_DB_DIR = "C:\\Users\\sushr\\BASIC_RAG\\chroma_db"
COLLECTION_NAME = "BasicRAG"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
def load_vector_store():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )
    return vector_store
def retrieve_relevant_documents(vector_store, query):
    relevant_docs = vector_store.similarity_search(query,3)
    return relevant_docs
def generate_answer(relevant_docs, query):
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

Context: {context}
Question: {query}
Answer : 
""" 
    response = llm.invoke(prompt)
    return response.content

def print_source(documents):
    """
    Print the source of each document in the list.
    """
    print("\nSources used:")
    for index, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "Unknown page")
        print(f"\nSource {index}:")
        print(f"  Source: {source}")
        print(f"  Page: {page}")
        print(f"Text preview: {doc.page_content[:300]}...")

def main():
    if len(sys.argv) < 2:
        print("Please provide a question.")
        print("Example: python query.py \"What is ISO 27001?\"")
        return
    query = " ".join(sys.argv[1:])
    vector_store = load_vector_store()
    relevant_docs = retrieve_relevant_documents(vector_store, query)
    if not relevant_docs:
        print("No relevant documents found.")
        return
    answer = generate_answer(relevant_docs, query)
    print(f"Answer: {answer}")
    print_source(relevant_docs)

if __name__ == "__main__":
    main()