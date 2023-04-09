from .models import Player, PlayerID
from ..schema import Question
from asyncio import sleep
from dataclasses import dataclass

"""
Each game instance contains currently connected players.
"""


kPOINTS = 1_000


@dataclass
class PlayerInfo:
    choice: str = ""
    score: int = 0


GameID = str


class Game:
    def __init__(self, host_id: PlayerID):
        self.current_question_id = 0
        self.state: str | None = "LOBBY"
        self.players: list[Player] = []
        self.questions: list[Question] = []
        self.player_info: dict[PlayerID, PlayerInfo] = dict()
        self.time = 0
        self.p_count = 0
        self.host_id = host_id

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    async def game_loop(self):
        self.state = "PLAY"
        while self.state != "FINISHED":
            await sleep(1)
            self.time += 1
            answered = [
                sum(
                    [
                        1 if len(pinfo.choice) else 0
                        for pid, pinfo in self.player_info.items()
                    ]
                )
            ]

            if self.time >= 30 or answered == len(self.players):
                await self.next_question()
                self.time = 0

    async def add_player(self, player: Player):
        player.player_id = self.p_count
        self.p_count += 1

        self.players.append(player)

        if player.socket:
            as_json = str(player.dict())
            await player.socket.send_text(as_json)

    async def remove_player(self, player: Player):
        self.players.remove(player)
        if player.socket:
            await player.socket.send_text("LEAVE")

    async def add_player_choice(self, player_id, choice):
        self.player_info[player_id].choice = choice

    async def next_question(self):
        self.check_answer()
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            self.state = "FINISHED"
            await self.broadcast("GAMEOVER")
            self.players[self.host_id].socket.send_text(self.player_info)
            return

        for pid, _ in self.player_info.items():
            self.player_info[pid].choice = ""

        await self.broadcast("NEXTQUESTION")

    async def broadcast(self, message: str):
        for player in self.players:
            if player.socket is None:
                continue  # HACK: for dev
            try:
                await player.socket.send_text(message)
            except:
                print("Removing player: ", player)
                self.players.remove(player)

    def check_answer(self):
        for player_id in self.player_info.keys():
            player_choice = self.player_info[player_id].choice
            if player_choice == self.questions[self.current_question_id].answer:
                self.player_info[player_id].score += kPOINTS

        # for player_id in self.player_info.keys():
        #     if (
        #         self.player_info[player_id].choice
        #         == self.questions[self.current_question_id].correct
        #     ):
        #         self.player_info[player].score += 1000


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""
