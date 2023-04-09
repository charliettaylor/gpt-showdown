from Player import Player

"""
Each game instance contains currently connected players.
"""

GameID = str


class Game:
    def __init__(self):
        self.current_question_id = 0
        self.state: str | None = None
        self.players: list[Player] = []

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""
