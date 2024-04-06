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

# Initialize text splitter and embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# Celery setup
redis = Redis(host="20.41.249.147", port=6379, username="default", password="admin", db=0)
app = Celery('celery_chroma_ingest', broker='redis://20.41.249.147:6379/0', backend="redis://20.41.249.147:6379/0")
# print(app)
# app.conf.enable_utc = False

# app = Celery('tasks')
# app.config_from_object('tasks.config')

# Initialize Chroma DB client
chroma_client = chromadb.PersistentClient(path="vector_storage")
collection = chroma_client.get_or_create_collection(name="pdf_database")
# print(collection)

# PDF to text
def pdf_to_text(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    pdf_file.close()
    return text

# Initialize text splitter and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
# print(embeddings)

# Process each PDF in the ./uploads directory
# @app.task(name="pdf_chroma_ingest.process_files")
@app.task
def process_files():
    uploads_dir = 'uploads'
    for filename in os.listdir(uploads_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(uploads_dir, filename)

            # Split text into chunks
            text = pdf_to_text(file_path)
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

            collection.add(embeddings=embeddings_list,
                           documents=documents_list,
                           ids=ids_list)
            logger.info(f"Stored {filename} in vector database")

            print("------")
            print(collection)

if __name__ == "__main__":
    process_files.delay()

# run using celery -A celery_chroma_ingest worker --loglevel=INFO 