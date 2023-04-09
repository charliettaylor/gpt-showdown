from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from assistant import Assistant
from db import (
    create_schema,
    get_choice_by_id,
    get_question_by_id,
    insert_choice,
    insert_question,
)
from parse_gpt import parse_gpt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

# Create a new gpt instance per game id
GameID = str
gpt_instances: defaultdict[GameID, Assistant] = defaultdict(lambda: Assistant())

active_games = set(["AAA"])


# create tables on startup
create_schema()


@app.get("/")
async def root():
    return {"message": "gpt showdown :)"}


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


async def get_gpt_response(game_id: GameID, question_id: str):
    """
    Query database and ask GPT what it thinks the answer is.
    """
    # ensure active game
    if game_id not in active_games:
        return {"message": "Game not active."}

    # TODO: query db for question text
    totally_real_db_query = lambda *, qid: "What is 2+2?"  # pyright: ignore

    question_text = totally_real_db_query(qid=question_id)

    gpt = gpt_instances[game_id]
    initial_gpt_response = gpt.write_message(role="user", content=question_text)
    parsed_gpt_response = parse_gpt(
        initial_gpt_response
    )  # to the form "A" or "B" or "C" or "D"

    return {"message": "GPT successfuly answered.", "gpt_response": parsed_gpt_response}
