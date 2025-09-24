import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------
# Load GEMINI API KEY from .env
# -----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Google Generative AI
genai.configure(api_key=api_key)

# -----------------------------
# Initialize LLM (Gemini model)
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key
)

# -----------------------------
# Load vectorstore
# -----------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

try:
    db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
except Exception as e:
    raise RuntimeError(f"⚠️ Error loading vectorstore: {e}")

# -----------------------------
# Create RetrievalQA chain
# -----------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
)

# -----------------------------
# Function to get answer
# -----------------------------
def get_answer(question: str) -> str:
    """Return an answer for a given question using RAG pipeline"""
    result = qa_chain.invoke({"query": question})
    return result["result"]

# -----------------------------
# Quick test
# -----------------------------
if __name__ == "__main__":
    q = "What are the best products for dry hair?"
    print("❓ Question:", q)
    print(" Answer:", get_answer(q))
