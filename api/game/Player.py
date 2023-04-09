from pydantic import BaseModel

"""
Each player instance contains information about currently connected users over TCP.
"""


class Player(BaseModel):
    nickname: str
    player_id: int
    game_id: str
    choice: str
