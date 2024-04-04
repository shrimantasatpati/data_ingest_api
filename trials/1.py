# from fastapi import FastAPI
# import uvicorn
# from redis import Redis
# from celery import Celery
# from data_ingestion import fetch_data, ingest_data_into_vector_store
# from config import settings

# app = FastAPI()
# redis = Redis()
# celery = Celery(__name__,
#                 broker=settings.CELERY_BROKER_URL,
#                 backend=settings.CELERY_RESULT_BACKEND)

# @app.post("/ingest")
# async def ingest_data(data_source: dict):
#     # """
#     # Endpoint to ingest data from different sources.

#     # Args:
#     #     data_source (dict): A dictionary containing the following keys:
#     #         - source_type (str): Type of the source (local, website, cloud)
#     #         - source_location (str): Specific source location (path, URL, etc.)

#     # Returns:
#     #     dict: A dictionary containing the task ID of the Celery task.
#     # """
#     task = ingest_data_task.delay(data_source)
#     return {"task_id": task.id
#             # "source_type": data_source["source_type"]
#             # "source_location": data_source["source_location"]
#             }

# @celery.task
# def ingest_data_task(data_source):
#     source_type = data_source['source_type']
#     source_location = data_source['source_location']

#     data = fetch_data(source_type, source_location)
#     ingest_data_into_vector_store(data)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)


# # # Start the Celery worker
# # celery -A main.celery worker --loglevel=info

# # {"source_type": "local", 
# # "source_location": "C:\\Users\\shrimantas\\Downloads\\ikegai_platform"}

# app.py


# import os
# import requests
# import redis

# # Initialize Redis Stack connection
# redis_stack = redis.Redis()

# def fetch_data(source_type, source_location):
#     """
#     fetch data from different sources
#     (local folder, cloud location, website) to ingest into the vector store

#     {args}:

#     {returns}:
    
#     """

#     if source_type == 'local':
#         return fetch_from_local_folder(source_location)
#     elif source_type == 'cloud':
#         return fetch_from_cloud_location(source_location)
#     elif source_type == 'website':
#         return fetch_from_website(source_location)
#     else:
#         raise ValueError(f"Invalid source type: {source_type}")
    


# def fetch_from_local_folder(folder_path):
#     data = []
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             with open(file_path, 'r') as f:
#                 data.append(f.read())
#     return data

# def fetch_from_cloud_location(cloud_location):
#     pass

# def fetch_from_website(url):
#     response = requests.get(url)
#     return [response.text]

# def ingest_data_into_vector_store(data):
#     """ 
#     Stores ingested data into the vector database
#     Support sync updates and batch processing
#     """
#     # Batch processing
#     for item in data:
#         process_item(item)

# def process_item(item):
#     # Check if the item already exists in the vector store
#     item_id = hash(item)
#     existing_item = redis_stack.get(item_id)

#     if existing_item:
#         # Item exists, perform sync update
#         redis_stack.set(item_id, item)
#     else:
#         # Item doesn't exist, insert it
#         redis_stack.set(item_id, item)

# def hash(item):
#     """
#     Helper function to generate a unique hash for the item.
#     You can modify this function based on your data representation.
#     """
#     return hash(str(item))