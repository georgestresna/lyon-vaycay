from fastapi import FastAPI
import json

with open("fin_data.json", "r") as file:
    data = json.load(file)

app = FastAPI()

@app.get("/")
def root():
    return data

# uvicorn web:app --reload