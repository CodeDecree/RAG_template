from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.assistant import Assistant
from app.services.doc_uploader import DocUploader
from fastapi.staticfiles import StaticFiles

UPLOAD_DIR = "./data"

app = FastAPI()
uploader = DocUploader(upload_dir="data")
assistant = Assistant(data_dir='./data/')
templates = Jinja2Templates(directory="templates")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home Page", "message": "Welcome to FastAPI with Jinja2!"})

@app.get("/assistant")
def read_root(message: str = None):
    if message:
        return {"response": assistant.getResponse(message)}
    return {"response": "No message provided"}

@app.post("/upload")
async def doc_upload(file: UploadFile = File(...)):
    """
    Uploads a document and saves it to the server.

    :param file: Uploaded file from request
    :return: JSON response with file path or error message
    """
    try:
        file_path = uploader.save_file(await file.read(), file.filename)  
        return {"message": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/delete/{filename}")
def delete_file(filename: str):
    """
    Deletes a file from the storage directory.

    :param filename: Name of the file to delete
    :return: JSON response confirming deletion or error message
    """
    if uploader.delete_file(filename):
        return {"message": "File deleted successfully"}
    return {"error": "File not found"}