import streamlit as st
import requests 
API_URL = "http://127.0.0.1:8000/ask"
UPLOAD_API_URL = "http://127.0.0.1:8000/upload"
st.set_page_config(
    page_title = "Basic_RAG",
    page_icon = ":bar_chart:",
    layout = "centered"
)
st.title(" Basic RAG Chatbot")
st.write("Ask questions from your ingested PDF documents.")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
question = st.text_input("Enter your question:")
if uploaded_file is not None:
    if st.button("Upload PDF File for Knowledge Base"):
        with st.spinner("Uploading and ingesting the PDF..."):
            files = {
                "file" : (
                    uploaded_file.name, 
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }
            response = requests.post(
                UPLOAD_API_URL,
                files=files
            )
            if response.status_code == 200 : 
                data = response.json()
                st.success(data["message"])
                st.write(f"File name: {data.get('file_name')}")
                st.write(f"Pages loaded: {data.get('pages_loaded')}")
                st.write(f"Chunks created: {data.get('chunks_created')}")
                st.write(f"File size: {data.get('file_size')}")
            else:
                st.error("PDF upload failed.")
st.divider()
if st.button("Ask me"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching document and generating answer..."):
            response = requests.post(API_URL, json={"question": question})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Answer")
                st.write(data["answer"])
                st.subheader("Sources")
                for index, source in enumerate(data["sources"], start=1):
                    with st.expander(f"Source {index} - page {source['page']}"):
                        st.write(f"**File:** {source['source']}")
                        st.write(source["preview"])
            else :
                st.error("Something went wrong while calling the API.")