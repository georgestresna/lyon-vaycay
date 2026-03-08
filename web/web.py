import json
import os
from fastapi import FastAPI

from web.details import to_display, final_data


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
TRIPS_FILE = os.path.join(PROJECT_ROOT, "json_files", "trips_rated.json")

with open(TRIPS_FILE, "r") as file:
    data = json.load(file)
trimmed = to_display(data)

app = FastAPI()

@app.get("/")
def root():
    return final_data(data, trimmed)

# uvicorn /web/web:app --reload