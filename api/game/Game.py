from ..assistant import Assistant
from .models import Player, PlayerID, Event
from ..schema import McQuestionDTO, Question, McQuestion
from asyncio import create_task, sleep, run
from ..db import get_questions_by_quiz  # HACK: for debugging GPT integration
from dataclasses import dataclass
from ..parse_gpt import parse_gpt
import json
from asyncio import create_task, gather, run

"""
Each game instance contains currently connected players.
"""


kPOINTS = 1_000
kGPT_ID = 1337


GameID = str


class Game:
    def __init__(self, host_id: PlayerID):  # HACK: don't need host_id here... always 0
        self.current_question_id = 0
        self.state: str | None = "LOBBY"
        self.players: list[Event] = []
        self.choices: dict[PlayerID, str] = dict()
        self.questions: list[McQuestion] = []
        self.time = 0
        self.p_count = 0
        self.host_id = host_id
        self.gpt = None

    def __repr__(self):
        out = f"Game[{self.state=}, {self.players=}]"
        return out

    async def setup_gpt(self, host_event: Event):
        gpt_event = Event(nickname="GPT", action="JOIN", player_id=kGPT_ID, socket=None)

        self.gpt = Assistant()

        self.players.append(gpt_event)

    async def game_loop(self):
        self.state = "PLAY"
        await self.broadcast("COUNTDOWN", 3)
        await self.broadcast("QUESTION")
        while self.state != "FINISHED":
            if kGPT_ID not in self.choices.keys():
                gpt_answer = await self.get_gpt_response()
                self.choices[kGPT_ID] = gpt_answer
                # print(self.choices)

            await sleep(1)
            # await self.broadcast("TIME", 30 - self.time)
            self.time += 1

            if self.time >= 30 or len(self.choices.keys()) == len(self.players) - 1:
                await self.next_question()
                self.time = 0

    async def add_player(self, player: Player):
        player.player_id = self.p_count
        self.p_count += 1

        self.players.append(player)
        await self.broadcast("LOBBY")

    async def start_lobby(self):
        await self.broadcast("LOBBY")
        task = create_task(self.setup_gpt(self.players[0]))
        await gather(task)
        # t = Thread(target=self.setup_gpt, args=[self.players[0]])
        # t.run()

    # async def remove_player(self, player: Player):
    #     self.players.remove(player)
    #     if player.socket:
    #         await player.socket.send_text("LEAVE")
    #         await self.notify_host(json.dumps(player.dict()))

    async def add_player_choice(self, player_id, choice):
        self.choices[player_id] = choice
        # print("\n\n\n\nAHHHH: ", self.choices, "\n\n\n")

    async def handle_end_game(self):
        self.state = "FINISHED"
        await self.broadcast("GAMEOVER")

    async def next_question(self):
        self.check_answer()
        await self.broadcast("ANSWER")
        await sleep(3)
        self.current_question_id += 1
        if self.current_question_id >= len(self.questions):
            await self.handle_end_game()
            return

        self.choices.clear()

        await self.broadcast("COUNTDOWN", 3)
        await self.broadcast("QUESTION")

    async def broadcast(self, state: str, countdown: int = None):
        for player in self.players:
            if player.player_id == kGPT_ID:
                continue
            # if state == "QUESTION" and player.player_id == kGPT_ID:
            #     gpt_answer = await self.get_gpt_response()
            #     self.choices[kGPT_ID] = gpt_answer
            #     print(self.choices)

            try:
                assert (
                    player.socket is not None and player.player_id is not kGPT_ID
                ), "Error: player socket is invalid"
                dic = player.dict()
                del dic["socket"]
                copy = Event(**dic)
                copy.socket = None
                copy.state = state
                copy.player_count = len(self.players)
                copy.choice = None

                if state == "COUNTDOWN":
                    copy.countdown = countdown
                    await player.socket.send_text(json.dumps(copy.dict()))
                    continue
                elif state == "QUESTION":
                    x = self.questions[self.current_question_id]
                    copy.question = McQuestionDTO(text=x.question, choices=x.choices)

                elif state == "GAMEOVER":
                    copy.leaderboard = [
                        {"nickname": x.nickname, "score": x.score}
                        for x in list(
                            sorted(self.players, key=lambda x: x.score, reverse=True)
                        )  # [: min(3, len(self.players))]
                    ]
                elif state == "ANSWER":
                    copy.answer = self.questions[self.current_question_id].answer
                    copy.leaderboard = [
                        {"nickname": x.nickname, "score": x.score}
                        for x in list(
                            sorted(self.players, key=lambda x: x.score, reverse=True)
                        )  # [: min(3, len(self.players))]
                    ]

                await player.socket.send_text(json.dumps(copy.dict()))
            except Exception as e:
                print("Error: ", e)
                print("Removing player: ", player)
                self.players.remove(player)

        if countdown is not None and countdown > 0 and state == "COUNTDOWN":
            await sleep(1)
            await self.broadcast(state, countdown - 1)

    def check_answer(self):
        for i, player in enumerate(self.players):
            if player.player_id not in self.choices.keys():
                continue
            player_choice = self.choices[player.player_id]
            if player_choice == self.questions[self.current_question_id].answer:
                self.players[i].score += kPOINTS

    # TODO: move this to different file

    async def get_gpt_response(self):
        """
        Query database and ask GPT what it thinks the answer is.
        """

        current_question = self.questions[self.current_question_id]
        dto = McQuestionDTO(
            text=current_question.question, choices=current_question.choices
        )

        formatted_for_gpt = dto.text
        for choice in dto.choices:
            if choice.value == "None":
                continue
            formatted_for_gpt += f"\n{choice.choice}: {choice.value}"

        initial_gpt_response = self.gpt.write_message(
            role="user", content=formatted_for_gpt
        )
        parsed_gpt_response = await parse_gpt(
            initial_gpt_response
        )  # to the form "A" or "B" or "C" or "D"

        debug = {
            "message": "GPT successfuly answered.",
            "gpt_response": parsed_gpt_response,
            "initial_gpt_response": initial_gpt_response,
            "question_text": formatted_for_gpt,
        }
        assert parsed_gpt_response in "ABCD", "Bad GPT Response"

        print("GPT-DEBUG ", debug)
        return parsed_gpt_response


"""
on...

join -> send nickname, game_id
leave -> send nickname, game_id
"""

if __name__ == "__main__":
    g = Game(host_id=0)
    run(g.get_gpt_response())
