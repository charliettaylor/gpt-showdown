from pydantic import BaseModel
from fastapi import WebSocket
from ..schema import McQuestionDTO

"""
Each player instance contains information about currently connected users over TCP.
"""
PlayerID = int


class Player(BaseModel):
    nickname: str
    player_id: PlayerID | None = None
    game_id: str | None = None
    quiz_id: int
    choice: str | None = None
    score: int = 0
    socket: WebSocket | None = None

    class Config:
        arbitrary_types_allowed = True


class PlayerDTO(BaseModel):
    nickname: str
    score: int


class Event(Player):
    # JOIN, LEAVE, SUBMIT
    action: str
    # LOBBY, COUNTDOWN, QUESTION, ANSWER, GAMEOVER
    state: str = "LOBBY"
    question: McQuestionDTO | None = None
    answer: str | None = None
    leaderboard: list[PlayerDTO] | None = None
    player_count: int = 0
    error: str | None = None
