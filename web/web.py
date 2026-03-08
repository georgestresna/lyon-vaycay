from fastapi import FastAPI
from details import to_display, final_data
import json

with open("../json_files/trips_rated.json", "r") as file:
    data = json.load(file)
trimmed = to_display(data)

app = FastAPI()

@app.get("/")
def root():
    return final_data(data, trimmed)

# uvicorn /web/web:app --reload