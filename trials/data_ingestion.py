import os
import hashlib

class VectorStore:
    def __init__(self, store_dir):
        self.store_dir = store_dir
        os.makedirs(store_dir, exist_ok=True)

    def ingest(self, data, filename):
        # Calculate the hash of the data
        data_hash = hashlib.sha256(data.encode()).hexdigest()

        # Check if the data already exists in the store
        existing_data_path = os.path.join(self.store_dir, f"{data_hash}.txt")
        if os.path.exists(existing_data_path):
            print(f"Data with hash {data_hash} already exists, skipping ingestion")
            return

        # Store the data in the project directory
        data_path = os.path.join(self.store_dir, f"{data_hash}.txt")
        with open(data_path, 'w') as file:
            file.write(data)

        print(f"Ingested data with filename: {filename}, hash: {data_hash}")


# from celery import Celery
# import os
# from data_ingestion import VectorStore

# # Initialize Celery
# app = Celery('tasks', broker='redis://localhost:6379/0')

# # Initialize vector store
# upload_dir = 'upload'
# project_dir = 'project'
# vector_store = VectorStore(project_dir)

# @app.task
# def monitor_upload_directory():
#     while True:
#         for filename in os.listdir(upload_dir):
#             filepath = os.path.join(upload_dir, filename)
#             if os.path.isfile(filepath):
#                 try:
#                     with open(filepath, 'r') as file:
#                         data = file.read()
#                         vector_store.ingest(data, filename)
#                     os.remove(filepath)
#                 except Exception as e:
#                     print(f"Error ingesting file {filepath}: {e}")


# from fastapi import FastAPI, BackgroundTasks
# import uvicorn
# from celery_worker import monitor_upload_directory

# app = FastAPI()

# @app.lifespan("startup")
# async def start_monitoring_upload_directory():
#     monitor_upload_directory.delay()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)
