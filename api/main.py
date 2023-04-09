from collections import defaultdict
import json
import logging

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .assistant import Assistant
from .db import create_schema, insert_choice, insert_question, insert_quiz
from .parse_gpt import parse_gpt
from .schema import CreateQuiz
from .game.Manager import Manager
from .game.models import Event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a new gpt instance per game id
GameID = str
gpt_instances: defaultdict[GameID, Assistant] = defaultdict(lambda: Assistant())

active_games = set(["AAA"])


# create tables on startup
create_schema()


@app.get("/")
async def root():
    return {"message": "gpt showdown :)"}


@app.post("/api/quiz")
async def create_quiz(quiz: CreateQuiz):
    quiz_id = insert_quiz(quiz.name)

    if quiz_id is None:
        raise HTTPException(status_code=400, detail="Quiz not created")

    for question in quiz.questions:
        id = insert_question(quiz_id, question)
        assert id is not None, "Error: Bad ID retrieved"
        for choice in question.choices:
            insert_choice(id, choice)

    return {"message": "Quiz created"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    man = Manager.get_instance()
    assert man is not None, "Error: Manager is none in WebSocket endpoint!"
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            as_json = json.loads(data)
            as_json["socket"] = websocket
            event = Event(**as_json)
        except:
            await websocket.send_text(
                "Invalid JSON in WebSocket body or Invalid Event model"
            )
            logging.info("Invalid JSON")
            return

        await man.dispatch(event=event)


# TODO: move this to different file
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
