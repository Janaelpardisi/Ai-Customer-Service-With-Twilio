🤖 AI Customer Service with Twilio & FastAPI

This project demonstrates how to build an AI-powered customer service system using:
- FastAPI to create a lightweight and high-performance API.  
- LangChain + HuggingFace Embeddings for intelligent retrieval and answering from the knowledge base.  
- Twilio WhatsApp Sandbox for WhatsApp integration and automated customer replies.  
- FAISS Vector Store to store and retrieve data efficiently.  



 📌 Features
✅ Answer customer queries directly from WhatsApp.  
✅ Simple web interface built with HTML + Jinja.  
✅ Knowledge base stored in a CSV file and converted into vectors.  
✅ Flexible to add new data easily.  
✅ Scalable with future support for MongoDB or any other database.  



 🛠️ Requirements
Before running the project, make sure you have:
- Python 3.10+  
- All required Python libraries from `requirements.txt`  

📌 Install dependencies:
bash
pip install -r requirements.txt

🚀 Run Locally

Start the FastAPI server:

uvicorn app:app --reload


Server will be available at:

http://127.0.0.1:8000


Open the link in your browser to access the web interface.

💬 WhatsApp Integration (Twilio)

Sign up for Twilio.

Go to Twilio WhatsApp Sandbox.

Connect your local server using a tunneling tool such as ngrok or localtunnel:

ngrok http 8000


or

lt --port 8000


Copy the generated public URL and paste it into Twilio’s Inbound Webhook.

Send a message from your phone to the Twilio sandbox number and enjoy instant AI responses 🚀.

📂 Project Structure
.
├── app.py                 # Main FastAPI application
├── rag_ai.py              # AI logic (LangChain + Embeddings)
├── build_data.py          # Prepare knowledge data from CSV
├── build_vectorstore.py   # Build FAISS vector database
├── knowledge.csv          # Knowledge base file
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Simple web interface
└── vectorstore/           # FAISS storage files

📌 Future Improvements

Use MongoDB or other databases for storing Q&A.

Improve responses with more advanced LLMs such as GPT-4 or LLaMA.

Add multi-language support 🌍.

Develop an admin dashboard for monitoring and analytics.

✨ Developer

👩‍💻 Jana Ashraf
📌 GitHub Profile
