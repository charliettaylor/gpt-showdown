from collections import defaultdict
from .Game import Game, GameID
from .models import Event, PlayerID
from random import choice
from string import ascii_uppercase
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

        self.hosts: dict[PlayerID, Game] = dict()
        self.games: dict[GameID, Game] = dict()
        Manager.__instance = self

    def generate_game_id(self):
        random_id = "".join([choice("0123456789") for _ in range(3)])
        if random_id in self.games.keys():
            return self.generate_game_id()

        return random_id  # [A-Z]{3}

    def create_game(self, host_id: int):
        game_id = self.generate_game_id()
        game = Game(host_id)
        self.games[game_id] = game
        self.hosts[host_id] = game_id

    async def dispatch(self, event: Event):
        print(event)
        if event.action == "CREATE":
            # player needs id
            event.player_id = 0
            # make the new game
            self.create_game(event.player_id)
            # make host have id of game
            event.game_id = self.hosts[event.player_id]

            game = self.games[event.game_id]
            await game.add_player(event)
            return

        if event.game_id not in self.games.keys():
            return

        game = self.games[event.game_id]
        if event.action == "JOIN":
            await game.add_player(event)
        elif event.action == "SUBMIT":
            await game.add_player_choice(event)
        elif event.action == "LEAVE":
            await game.remove_player(event)

        # admin only stuff
        if (
            event.player_id not in self.hosts.keys()
            or self.hosts[event.player_id] != event.game_id
        ):
            return

        if event.action == "START":
            Thread(await game.game_loop())


if __name__ == "__main__":
    man = Manager.get_instance()
    man.create_game()
    print(man.games)
