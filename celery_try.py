import os
import datetime
from celery import Celery
from celery.schedules import crontab
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.documents.base import Document
import PyPDF2
from redis import Redis
import logging
import os
import PyPDF2
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# Celery setup
redis = Redis(host="localhost", port=6379, db=0)
app = Celery('file_embeddings', broker='redis://localhost:6379/0', backend="redis://localhost:6379/0")
# app.conf.enable_utc = False

# Initialize Chroma DB client
# chroma_client = chromadb.PersistentClient(path="vector_storage")
# collection = chroma_client.get_or_create_collection(name="file_embeddings")

# Function to convert PDF to text
def pdf_to_text(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range( len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    pdf_file.close()
    return text

# Initialize text splitter and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")

# Initialize Chroma DB client
client = chromadb.PersistentClient(path="./db")
collection = client.create_collection(name="file_embeddings")

# Process each PDF in the ./input directory
@app.task(name="file_embeddings.process_files")
def process_files():
    for filename in os.listdir('./uploads'):
        if filename.endswith('.pdf'):
            # Convert PDF to text
            text = pdf_to_text(os.path.join('./uploads', filename))

            # Split text into chunks
            chunks = text_splitter.split_text(text)

            # Convert chunks to vector representations and store in Chroma DB
            documents_list = []
            embeddings_list = []
            ids_list = []
            
            for i, chunk in enumerate(chunks):
                vector = embeddings.embed_query(chunk)
                
                documents_list.append(chunk)
                embeddings_list.append(vector)
                ids_list.append(f"{filename}_{i}")
            
            
            collection.add(
                embeddings=embeddings_list,
                documents=documents_list,
                ids=ids_list
            )

app.conf.beat_schedule = {
    "process-files": {
        "task": "file_embeddings.process_files",
        "schedule": crontab(minute="0.01",
                            hour="0"
                            # day="*"
                            )  # Run every minute
    }
}

if __name__ == "__main__":
    # Start the Celery beat process
    app.start()