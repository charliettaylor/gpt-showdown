from pydantic import BaseModel
from fastapi import WebSocket

"""
Each player instance contains information about currently connected users over TCP.
"""
PlayerID = int

class Player(BaseModel):
    nickname: str = ""
    player_id: PlayerID = 0
    game_id: str = "000"
    choice: str = ""
    _socket: WebSocket | None = None


class Event(Player):
    # JOIN, LEAVE, SUBMIT
    action: str
