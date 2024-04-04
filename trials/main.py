# from fastapi import FastAPI, File, UploadFile, BackgroundTasks
# import uvicorn
# from celery_worker import process_file
# from redis import Redis
# import os

# app = FastAPI()
# redis = Redis(host="localhost", port=6379, db=0)

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
#     file_path = f"uploads/{file.filename}"
#     with open(file_path, "wb") as buffer:
#         contents = await file.read()
#         buffer.write(contents)

#     background_tasks.add_task(process_file.delay, file_path)
#     return {"message": "File upload successful"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)


from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import uvicorn
from celery_worker import process_file
import os
from redis import Redis

app = FastAPI()
redis = Redis(host="localhost", port=6379, db=0)

@app.post("/upload_multiple_files")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)

    background_tasks.add_task(process_file.delay, file_path)
    return {"message": "File upload successful"}

@app.post("/upload_local_folder")
async def process_folder(folder_path: str, background_tasks: BackgroundTasks = BackgroundTasks()):
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                background_tasks.add_task(process_file.delay, file_path)
        return {"message": "Folder processing started"}
    else:
        return {"error": "Invalid folder path"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)