from pydantic import BaseModel
from fastapi import WebSocket

"""
Each player instance contains information about currently connected users over TCP.
"""
PlayerID = int


class Player(BaseModel):
    nickname: str = ""
    player_id: PlayerID | None = None
    game_id: str | None = None
    choice: str | None = None
    socket: WebSocket | None = None

    class Config:
        arbitrary_types_allowed = True


class Event(Player):
    # JOIN, LEAVE, SUBMIT
    action: str
