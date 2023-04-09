from collections import defaultdict
import json
import logging

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .assistant import Assistant
from .db import (
    create_schema,
    insert_choice,
    insert_question,
    insert_quiz,
    get_all_quizzes,
    get_all_quiz_categories,
)
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


@app.post("/quiz")
async def create_quiz(quiz: CreateQuiz):
    quiz_id = insert_quiz(quiz)

    if quiz_id is None:
        raise HTTPException(status_code=400, detail="Quiz not created")

    for question in quiz.questions:
        id = insert_question(quiz_id, question)
        assert id is not None, "Error: Bad ID retrieved"
        for choice in question.choices:
            insert_choice(id, choice)

    return {"message": "Quiz created"}


@app.get("/get_quizzes")
async def get_quizzes():
    return get_all_quizzes()


@app.get("/get_quiz_categories")
async def get_quiz_categories():
    return get_all_quiz_categories()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    man = Manager.get_instance()
    assert man is not None, "Error: Manager is none in WebSocket endpoint!"
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except:
            break

        try:
            as_json = json.loads(data)
            as_json["socket"] = websocket
            event = Event(**as_json)
        except:
            await websocket.send_text(Event(state="ERROR", error="Invalid JSON"))
            logging.info("Invalid JSON")
            break

        await man.dispatch(event=event)

    # handle leave
