Here’s a clean, professional, and user-friendly README.md for your MediBot project, including instructions about cloning, adding their own GROQ API key, running locally with uv, and a brief description:

# MediBot: RAG-based Medical Chatbot

MediBot is a Retrieval-Augmented Generation (RAG) chatbot designed to answer medical questions using information from PDF documents. It leverages **Groq LLM** for natural language understanding and **FAISS** for vector-based retrieval of document chunks.  

---

## ⚠️ Important
Before cloning and running this project, you **must provide your own GROQ API Key**. This is required for the chatbot to connect with the Groq LLM.  

1. Sign up at [Groq](https://groq.com/) and get your API Key.  
2. Create a `.env` file in the project root:  

```env
GROQ_API_KEY=your_groq_api_key_here

📥 Clone the Project
git clone https://github.com/AbdulRazzaq007/medibot_.git
cd medibot_

🛠 Setup & Run Locally

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows


Install dependencies using UV:

uv install
uv export -f requirements.txt -o requirements.txt
pip install -r requirements.txt


Run the chatbot locally:

uv run medibot.py


Open your browser at:

http://localhost:8501/


You will see the MediBot interface where you can type your medical questions.

📂 Project Structure

medibot.py – Main Streamlit app for the chatbot.

connect_memory_with_llm.py – Connects the LLM with FAISS vector store.

create_memory_for_llm.py – Processes PDFs and creates embeddings for FAISS.

data/ – Folder to store PDF documents.

vectorstore/ – FAISS database for embeddings.

.env – Environment variables (GROQ API key).

💡 Usage Notes

Make sure the .env file is never pushed to public repos with real API keys.

Use your own PDFs in the data/ folder for training the chatbot.

For large document sets, the FAISS database may take time to generate.

🔗 Links

GitHub Repo: https://github.com/AbdulRazzaq007/medibot_.git

Local Streamlit App: http://localhost:8501/


