from .models import Player, Event
from ..schema import Question
from time import sleep

"""
Each game instance contains currently connected players.
"""

GameID = str


class Game:
    def __init__(self, host_id):
        self.current_question_id = 0
        self.state: str | None = "LOBBY"
        self.players: list[Player] = []
        self.questions: list[Question] = []
        self.current_choices = dict()
        self.time = 0
        self.p_count = 0

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    def game_loop(self):
        while self.state != "FINISHED":
            sleep(1)
            self.time += 1
            if self.time == 30 or len(self.current_choices) == len(self.players):
                self.next_question()
                self.time = 0

    def add_player(self, player: Player):
        player.player_id = self.p_count
        self.p_count += 1

        self.players.append(player)
        player._socket.send_text(player)

    def remove_player(self, player: Player):
        self.players.remove(player)
        player._socket.send_text("LEAVE")

    def add_player_choice(self, player_id, choice):
        self.current_choices[player_id] = choice

    def next_question(self):
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            self.state = "FINISHED"
            self.broadcast("GAMEOVER")
            return

        self.current_choices = dict()
        self.broadcast("NEXTQUESTION")

    def broadcast(self, message: str):
        for player in self.players:
            player._socket.send_text(message)


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""
