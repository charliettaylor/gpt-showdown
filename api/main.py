from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistant import Assistant
from fastapi.middleware.cors import CORSMiddleware

from db import (
    create_schema,
    insert_question,
    get_question_by_id,
    insert_choice,
    get_choice_by_id,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

# create tables on startup
create_schema()


@app.get("/")
async def root():
    return {"message": "gpt showdown :)"}


@app.get("/get_gpt_response")
async def get_gpt_response():
    pass


@app.get("/api/question/{id}")
async def get_question(id: int):
    return get_question_by_id(id)


@app.get("/api/choice/{id}")
async def get_choice(id: int):
    return get_choice_by_id(id)


@app.post("/api/question")
async def post_question(question: str, answer: str):
    q = insert_question(question, answer)

    if q:
      return {"message": "question added"}

    raise HTTPException(status_code=400, detail="Failed to add question")
        



@app.post("/api/choice")
async def post_choice(question_id: int, choice: str):
    c = insert_choice(question_id, choice)
    
    if c:
      return {"message": f"choice added to quesion {question_id}"}
    
    raise HTTPException(status_code=400, detail="Failed to add choice")
