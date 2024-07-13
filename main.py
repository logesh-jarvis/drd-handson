from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from claude_service import generate_coding_question
from typing import List

app = FastAPI()

class Topic(BaseModel):
    name: str

class TestCase(BaseModel):
    input: str
    expected_output: str

class CodingQuestion(BaseModel):
    question: str
    difficulty: str
    category: str
    hints: List[str]
    solution: str
    test_cases: List[TestCase]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/generate_question", response_model=CodingQuestion)
async def create_question():
    response = generate_coding_question()
    if response["question"].startswith("Error:"):
        raise HTTPException(status_code=500, detail=response["question"])
    return response