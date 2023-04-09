from .models import Player, Event, PlayerID
from api.schema import Question  # type: ignore
from asyncio import sleep


"""
Each game instance contains currently connected players.
"""

GameID = str


class Game:
    def __init__(self, host_id: PlayerID):
        self.current_question_id = 0
        self.state: str | None = "LOBBY"
        self.players: list[Player] = []
        self.questions: list[Question] = []
        self.current_choices = dict()  # TODO: What is this?
        self.time = 0
        self.p_count = 0

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    async def game_loop(self):
        self.state = "PLAY"
        while self.state != "FINISHED":
            await sleep(1)
            self.time += 1
            if self.time == 30 or len(self.current_choices) == len(self.players):
                await self.next_question()
                self.time = 0

    async def add_player(self, player: Player):
        player.player_id = self.p_count
        self.p_count += 1

        self.players.append(player)
        if player._socket:
            await player._socket.send_text(repr(player))  # TODO: JSON-ify

    async def remove_player(self, player: Player):
        self.players.remove(player)
        if player._socket:
            await player._socket.send_text("LEAVE")

    async def add_player_choice(self, player_id, choice):
        self.current_choices[player_id] = choice

    async def next_question(self):
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            self.state = "FINISHED"
            await self.broadcast("GAMEOVER")
            return

        self.current_choices = dict()
        await self.broadcast("NEXTQUESTION")

    async def broadcast(self, message: str):
        for player in self.players:
            if player._socket is None:
                continue  # HACK: for dev
            await player._socket.send_text(message)


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""
