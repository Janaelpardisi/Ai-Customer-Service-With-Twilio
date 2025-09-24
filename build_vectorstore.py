import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# load data
df = pd.read_csv("knowledge.csv")

# transform each question and answer to documents
documents = []
for _, row in df.iterrows():
    content = f"السؤال: {row['question']}\nالإجابة: {row['answer']}"
    documents.append(Document(page_content=content))

# create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# build a base knowledge
db = FAISS.from_documents(documents, embeddings)

# save a base knowledge
db.save_local("vectorstore")

print("build_vectorstore is built successfully")
