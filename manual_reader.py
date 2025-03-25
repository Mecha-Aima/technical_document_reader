import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import re

st.markdown("""
    <style>
    
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
            
    /* Set font for all elements */
    * {
        font-family: 'Open Sans', sans-serif !important;
    }
            
    
    /* Chat Input Styling */
    .stChatInput input {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #3A3A3A !important;
    }
            
    /* Custom Buttons */
    div.stButton > button {
        background-color: #00FFAA;
        color: #000000;
        border-radius: 10px;
        padding: 10px;
    }

    /* Change hover effect */
    div.stButton > button:hover {
        background-color: #00BB77;
        color: #FFFFFF;
    }
    
    /* User Message Styling */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #2E2E2E;
        border-radius: 15px;
        color: #E0E0E0;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Assistant Message Styling */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #3A3A3A;
        border-radius: 15px;
        color: #FFFFFF;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Avatar Styling */
    .stChatMessage .avatar {
        background-color: #00FFAA !important;
        color: #000000 !important;
    }
    
    /* Text Color Fix */
    .stChatMessage p, .stChatMessage div {
        color: #FFFFFF !important;
    }
    
    .stFileUploader {
        background-color: #1E1E1E;
        border: 1px solid #3A3A3A;
        border-radius: 5px;
        padding: 15px;
    }
    
    h1, h2 {
        color:rgb(125, 190, 255) !important;
    }
            
    h3 {
        color: #FFFFFF !important;
        font-weight: 300 !important;
        line-height: 1.5 !important;
    }
    </style>
    """, unsafe_allow_html=True)


PROMPT_TEMPLATE = """
You are a highly specialized assistant designed to process technical manuals nad product guides. Answer user queries based on following context.
You should provide concise, accurate, and helpful responses that help users understand complex information from the manuals.

Query: {user_query}
Context: {document_context}
Answer:
"""

@st.cache_resource
def get_embedding_model():
    return OllamaEmbeddings(model='deepseek-r1:1.5b')

@st.cache_resource
def get_llm():
    return OllamaLLM(model='deepseek-r1:1.5b')

PDF_PATH = 'document_store/manuals/'
EMBEDDING_MODEL = get_embedding_model()
DOCUMENT_DB = InMemoryVectorStore(embedding=EMBEDDING_MODEL)
LLM = get_llm()

def save_uploaded_file(file):
    file_path = PDF_PATH + file.name
    with open(file_path, 'wb') as f:
        f.write(file.getbuffer())
    return file_path

def load_pdf_documents(file_path):
    document_loader = PDFPlumberLoader(file_path)
    return document_loader.load()

def chunk_documents(raw_docs):
    text_processor = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        add_start_index=True,
    )
    return text_processor.split_documents(raw_docs)

def index_documents(chunks):
    DOCUMENT_DB.add_documents(chunks)

def find_related_docs(query):
    return DOCUMENT_DB.similarity_search(query)

def generate_answer(user_query, context_docs):
    context = "\n\n".join([doc.page_content for doc in context_docs])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = prompt | LLM
    response = response_chain.invoke({'user_query': user_query, 'document_context': context})
    clean_response = re.sub(r"<think>.*?</think>", '', response, flags=re.DOTALL)
    return clean_response.strip()

def main():
    st.title("📘 Manual Mate")
    st.markdown('### Simplify Your Technical Manuals: Parse, Extract, and Understand Complex Documentation with Ease.')
    st.markdown('---')

    uploaded_pdf = st.file_uploader(
        "📂 Upload your technical manual (PDF)",
        type='pdf',
        help="Select a pdf document for analysis",
        accept_multiple_files=False,
    )
    st.sidebar.title("Navigation")
    st.sidebar.radio("Go to", ["Home", "Upload Manual", "Ask Questions"])

    if uploaded_pdf:
        saved_path = save_uploaded_file(uploaded_pdf)
        raw_docs = load_pdf_documents(saved_path)
        doc_chunks = chunk_documents(raw_docs)
        index_documents(doc_chunks)

        st.success("✅ Document processed successfully! Ask your questions below.")
        user_input = st.chat_input("Ask question about document")
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)

            with st.spinner("Generating response..."):
                relevant_docs = find_related_docs(user_input)
                response = generate_answer(user_input, relevant_docs)

            with st.chat_message("assistant", avatar="🤖"):
                st.write(response)


if __name__ == "__main__":
    main()