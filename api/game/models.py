from pydantic import BaseModel
from fastapi import WebSocket

"""
Each player instance contains information about currently connected users over TCP.
"""


class Player(BaseModel):
    nickname: str
    player_id: int
    game_id: str
    choice: str
    _socket: WebSocket


class Event(Player):
    # JOIN, LEAVE, SUBMIT
    action: str
