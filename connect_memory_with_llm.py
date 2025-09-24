import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found. Put it in a .env file in project root.")

GROQ_MODEL_NAME = "llama-3.1-8b-instant"

llm = ChatGroq(
    model=GROQ_MODEL_NAME,
    temperature=0.5,
    max_tokens=512,
    api_key=GROQ_API_KEY,
)

DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
rag_chain = create_retrieval_chain(db.as_retriever(search_kwargs={"k": 3}), combine_docs_chain)

def main():
    user_query = input("Write Query Here: ")
    response = rag_chain.invoke({"input": user_query})
    print("RESULT:", response.get("answer"))
    print("\nSOURCE DOCUMENTS:")
    for doc in response.get("context", []):
        print(f"- {doc.metadata} -> {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()

