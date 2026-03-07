import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "templates", "index.html")
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/")
async def root(request: Request):
    dummy_data = {"page_title": "Lyon Vaycay - Best Deals"}

    return templates.TemplateResponse("index.html", {"request": request, "data": dummy_data})

    # uvicorn web:app --reload