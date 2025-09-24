import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

def load_pdf_files(data_path):
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def main():
    documents = load_pdf_files(DATA_PATH)
    if not documents:
        print("No PDFs found in", DATA_PATH)
        return
    text_chunks = create_chunks(documents)
    embedding_model = get_embedding_model()
    os.makedirs(DB_FAISS_PATH, exist_ok=True)
    db = FAISS.from_documents(text_chunks, embedding_model)
    db.save_local(DB_FAISS_PATH)
    print("Saved FAISS index to", DB_FAISS_PATH)

if __name__ == "__main__":
    main()
