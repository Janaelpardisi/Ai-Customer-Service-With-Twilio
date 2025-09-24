# app.py
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from twilio.rest import Client

# -----------------------------
# Load ENV variables
# -----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
USER_NUMBER = os.getenv("USER_PHONE_NUMBER")  

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# Initialize LLM & Vectorstore
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
)

# -----------------------------
# FastAPI & Templates
# -----------------------------
app = FastAPI(title="AI Customer Service")
templates = Jinja2Templates(directory="templates")

def get_answer(question: str) -> str:
    result = qa_chain.invoke({"query": question})
    return result["result"]

# -----------------------------
# Web Page Routes
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "answer": None})

@app.post("/ask", response_class=HTMLResponse)
def ask(request: Request, question: str = Form(...)):
    answer = get_answer(question)

    # Optional: send via Twilio WhatsApp
    if all([TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER, USER_NUMBER]):
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            to=f"whatsapp:{USER_NUMBER}",
            body=f"❓ {question}\n {answer}"
        )

    return templates.TemplateResponse(
        "index.html", {"request": request, "question": question, "answer": answer}
    )
