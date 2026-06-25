from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
from agent import*
from Task import*
from crewai import Process
import asyncio
from concurrent.futures import ThreadPoolExecutor
from jinja2 import FileSystemLoader, Environment


executor = ThreadPoolExecutor()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


tasks = [
    request_understand_task,
    pdf_reader_task,
    dependency_analysis_task,
    outline_builder_task,
    outline_checker_task,
    repair_task,
    lecturer_task,
]
agents = [
    Rqst_Understander,
    pdf_reader,
    dependency_analyzer,
    outline_builder,
    outline_checker,
    repair_agent,
    lecturer,
]


Professor_AI_crew = Crew(
    # include all the agents
    agents = agents,
    # include all the tasks in the order to be executed
    tasks = tasks,
    # add memory to the crew
    memory = False,
    process = Process.sequential,
    verbose = True,

)

def generate_lesson(user_request: str, pdf_path: str):

    pdf_reader_tool = PDFSearchTool(pdf=pdf_path)
    pdf_reader.tools = [pdf_reader_tool]

    result = Professor_AI_crew.kickoff(
        inputs={
            "user_request": user_request,
            "pdf_path": pdf_path,
        }
    )

    return str(result)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"result" : None})

@app.post("/teach", response_class=HTMLResponse)
async def teach(
    request: Request,
    user_request: str = Form(...),
    pdf_file: UploadFile = File(...),
):
    pdf_path =  UPLOAD_DIR / pdf_file.filename

    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(pdf_file.file, f)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        generate_lesson,
        user_request,
        str(pdf_path)
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
        },
    )
