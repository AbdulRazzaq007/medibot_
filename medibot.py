import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
load_dotenv() 

import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

def get_groq_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not found. Add it to .env or set the environment variable.")
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0.5, max_tokens=512, api_key=api_key)

def main():
    st.title("Ask Chatbot!")
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        st.chat_message(m['role']).markdown(m['content'])

    prompt = st.chat_input("Pass your prompt here")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({'role':'user','content':prompt})
        try:
            vectorstore = get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load vector store.")
                return

            llm = get_groq_llm()
            retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
            rag_chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={'k': 3}), combine_docs_chain)

            response = rag_chain.invoke({'input': prompt})
            result = response.get("answer", "No answer returned.")
            st.chat_message("assistant").markdown(result)
            st.session_state.messages.append({'role':'assistant','content':result})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
