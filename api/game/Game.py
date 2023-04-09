from .models import Player, PlayerID
from ..schema import McQuestionDTO, Question, McQuestion
from asyncio import sleep
from dataclasses import dataclass
import json

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
        self.questions: list[McQuestion] = []
        self.player_info: dict[PlayerID, PlayerInfo] = dict()
        self.time = 0
        self.p_count = 0
        self.host_id = host_id

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    async def countdown(self, amount: int) -> None:
        for i in range(amount, -1, -1):
            await self.broadcast(f"COUNTDOWN[{i}]")
            await sleep(1)

    async def game_loop(self):
        self.state = "PLAY"
        await self.broadcast("GAMESTART")
        await self.countdown(3)  # how long to wait before game start
        # send first question
        await self.broadcast_question()
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
            copy = Player(**player)
            copy.socket = None
            as_json = str(copy.dict())

            await player.socket.send_text(as_json)

    async def remove_player(self, player: Player):
        self.players.remove(player)
        if player.socket:
            await player.socket.send_text("LEAVE")

    async def add_player_choice(self, player_id, choice):
        self.player_info[player_id].choice = choice

    async def handle_end_game(self):
        self.state = "FINISHED"
        await self.broadcast("GAMEOVER")
        host_socket = self.players[self.host_id].socket
        assert host_socket is not None, "Error: lost player socket"
        # self.players[self.host_id].socket.send_text(self.player_info)
        await host_socket.send_text(str(self.player_info))

    async def next_question(self):
        self.check_answer()
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            await self.handle_end_game()
            return

        for pid, _ in self.player_info.items():
            self.player_info[pid].choice = ""

        await self.broadcast("NEXTQUESTION")
        await self.countdown(2)
        await self.broadcast_question()

    async def broadcast_question(self):
        current_question = self.questions[self.current_question_id]
        dto = McQuestionDTO(
            question=current_question.question, choices=current_question.choices
        )
        await self.broadcast(json.dumps(dto.dict()))
        print("ANSWER: ", current_question.answer)

    async def broadcast(self, message: str):
        for player in self.players:
            try:
                assert player.socket is not None, "Error: player socket is invalid"
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
