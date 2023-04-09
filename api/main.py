from collections import defaultdict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistant import Assistant
from fastapi.middleware.cors import CORSMiddleware

from collections import defaultdict


from db import (
    create_schema,
    insert_quiz,
    insert_question,
    insert_choice,
)

from schema import CreateQuiz, CreateQuestion, CreateChoice

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from assistant import Assistant
from db import (
    create_schema,
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


# Create a new gpt instance per game id
GameID = str
gpt_instances: defaultdict[GameID, Assistant] = defaultdict(lambda: Assistant())

active_games = set(["AAA"])


@app.post("/api/quiz")
async def create_quiz(quiz: CreateQuiz):
    quiz_id = insert_quiz(quiz.name)

    if quiz_id is None:
        raise HTTPException(status_code=400, detail="Quiz not created")
    print("penis", quiz_id)
    for question in quiz.questions:
        id = insert_question(quiz_id, question)
        for choice in question.choices:
            insert_choice(id, choice)
    
    return {"message": "Quiz created"}


async def get_gpt_response(game_id: GameID, question_id: str):
    """
    Query database and ask GPT what it thinks the answer is.
    """
    # ensure active game
    if game_id not in active_games:
        return {"message": "Game not active."}

    # TODO: query db for question text
    totally_real_db_query = (
        lambda *, qid: "What is 2+2?\nChoices: A: 4 B: 6 C:9 D:0"
    )  # pyright: ignore

    totallY_real_db_query_two = lambda *, qid: "A"

    question_text = totally_real_db_query(qid=question_id)
    actual_answer = totallY_real_db_query_two(qid=question_id)

    gpt = gpt_instances[game_id]
    initial_gpt_response = gpt.write_message(role="user", content=question_text)
    parsed_gpt_response = parse_gpt(
        initial_gpt_response
    )  # to the form "A" or "B" or "C" or "D"

    return {
        "message": "GPT successfuly answered.",
        "gpt_response": parsed_gpt_response,
        "initial_gpt_response": initial_gpt_response,
        "question_text": question_text,
    }
