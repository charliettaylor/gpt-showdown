from .models import Player, PlayerID, Event
from ..schema import McQuestionDTO, Question, McQuestion
from asyncio import sleep
from dataclasses import dataclass
import json

"""
Each game instance contains currently connected players.
"""


kPOINTS = 1_000


GameID = str


class Game:
    def __init__(self, host_id: PlayerID):
        self.current_question_id = 0
        self.state: str | None = "LOBBY"
        self.players: list[Event] = []
        self.choices: dict[PlayerID, str] = dict()
        self.questions: list[McQuestion] = []
        self.time = 0
        self.p_count = 0
        self.host_id = host_id

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    async def game_loop(self):
        self.state = "PLAY"
        await self.broadcast("COUNTDOWN")
        await self.broadcast("QUESTION")
        while self.state != "FINISHED":
            await sleep(1)
            self.time += 1

            if self.time >= 30 or len(self.choices.keys()) == len(self.players):
                await self.next_question()
                self.time = 0

    async def add_player(self, player: Player):
        player.player_id = self.p_count
        self.p_count += 1

        self.players.append(player)
        await self.broadcast("LOBBY")

    async def start_lobby(self):
        await self.broadcast("LOBBY")

    # async def remove_player(self, player: Player):
    #     self.players.remove(player)
    #     if player.socket:
    #         await player.socket.send_text("LEAVE")
    #         await self.notify_host(json.dumps(player.dict()))

    async def add_player_choice(self, player_id, choice):
        self.choices[player_id] = choice

    async def handle_end_game(self):
        self.state = "FINISHED"
        await self.broadcast("GAMEOVER")

    async def next_question(self):
        self.check_answer()
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            await self.handle_end_game()
            return

        for pid in self.choices.keys():
            self.choices[pid].choice = ""

        await self.broadcast("COUNTDOWN")
        await self.broadcast("QUESTION")

    async def broadcast(self, state: str):
        for player in self.players:
            try:
                assert player.socket is not None, "Error: player socket is invalid"
                copy = Event(**player.dict())
                copy.socket = None
                copy.state = state
                copy.player_count = len(self.players)
                copy.choice = None

                if state == "COUNTDOWN":
                    for i in range(3, 0, -1):
                        copy.countdown = i
                        await player.socket.send_text(json.dumps(copy.dict()))
                        await sleep(1)
                    continue
                elif state == "QUESTION":
                    x = self.questions[self.current_question_id]
                    copy.question = McQuestionDTO(text=x.question, choices=x.choices)
                elif state == "GAMEOVER":
                    copy.leaderboard = list(
                        sorted(player, lambda x: x.score, reverse=True)
                    )[:3]
                elif state == "ANSWER":
                    copy.answer = self.questions[self.current_question_id].answer
                    copy.leaderboard = list(
                        sorted(player, lambda x: x.score, reverse=True)
                    )[:3]

                await player.socket.send_text(json.dumps(copy.dict()))
            except Exception as e:
                print("Error: ", e)
                print("Removing player: ", player)
                self.players.remove(player)

    def check_answer(self):
        for player_id in self.choices.keys():
            player_choice = self.choices[player_id].choice
            if player_choice == self.questions[self.current_question_id].answer:
                self.players[player_id].score += kPOINTS


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""
