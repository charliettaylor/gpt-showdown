from collections import defaultdict

from fastapi import WebSocket
from .Game import Game, GameID
from .models import Event, PlayerID
from ..db import get_questions_by_quiz
from random import choice, randint
from threading import Thread
import logging
import sys


"""
Manager holds all activate game instances.

Uses a Singleton design pattern.
"""

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Manager:
    __instance = None

    @staticmethod
    def get_instance():
        if Manager.__instance is None:
            Manager()
        return Manager.__instance

    def __call__(self):
        return Manager.get_instance()

    def __init__(self):
        if Manager.__instance is not None:
            raise Exception("This class is a singleton!")

        self.hosts: dict[PlayerID, GameID] = dict()
        self.games: dict[GameID, Game] = dict()
        Manager.__instance = self

    def generate_game_id(self):
        # random_id = "".join([choice("0123456789") for _ in range(3)])
        random_id = str(randint(1700, 2024))
        if random_id in self.games.keys():
            return self.generate_game_id()

        return random_id  # [A-Z]{3}

    def create_game(self, event: Event):
        game_id = self.generate_game_id()
        assert event.player_id is not None, "Error: invalid Player ID"
        game = Game(event.player_id)

        game.questions = get_questions_by_quiz(event.quiz_id)

        self.games[game_id] = game
        self.hosts[event.player_id] = game_id

    async def dispatch(self, event: Event):
        if event.action == "PING":
            assert event.socket is not None, "Error: socket broken"
            if event.game_id in self.games.keys():
                await event.socket.send_text("pong")
                return
            await event.socket.send_text('{"error": "Bad Game ID"}')
            return

        if event.action == "CREATE":
            # player needs id
            event.player_id = 0
            # make the new game
            self.create_game(event)
            # make host have id of game
            event.game_id = self.hosts[event.player_id]
            game = self.games[event.game_id]
            await game.add_player(event)
            await game.start_lobby()
            print(event)
            return

        if event.game_id not in self.games.keys():
            print("Game does not exist", event.game_id)
            assert event.socket, "Error: broken socket."
            copy = Event(**event.dict())
            copy.socket = None
            copy.state = "ERROR"
            copy.error = "Game does not exist"
            await event.socket.send_text(json.dumps(copy.dict()))
            return

        assert event.game_id is not None, "Error: game id is Invalid"
        game = self.games[event.game_id]

        if event.action == "JOIN":
            await game.add_player(event)
        elif event.action == "SUBMIT":
            await game.add_player_choice(event.player_id, event.choice)
        elif event.action == "LEAVE":
            await game.remove_player(event)

        print(event)
        # admin only stuff
        if (
            event.player_id not in self.hosts.keys()
            or self.hosts[event.player_id] != event.game_id  # type: ignore
        ):
            return

        if event.action == "START":
            Thread(await game.game_loop())


if __name__ == "__main__":
    man = Manager.get_instance()
