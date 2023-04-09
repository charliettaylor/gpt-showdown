from collections import defaultdict
from Game import Game, GameID
from random import choice
from string import ascii_uppercase

"""
Manager holds all activate game instances.

Uses a Singleton design pattern.
"""


class Manager:
    __instance = None

    @staticmethod
    def get_instance():
        return Manager.__instance

    def __init__(self):
        if Manager.__instance != None:
            raise Exception("Can't create more than one Manager instance (singleton)!")
        else:
            Manager.__instance = self

        self.games: dict[GameID, Game] = dict()

    def generate_game_id(self):
        random_id = "".join([choice("0123456789") for _ in range(3)])
        if random_id in self.games.keys():
            return self.generate_game_id()

        return random_id  # [A-Z]{3}

    def create_game(self):
        game_id = self.generate_game_id()
        game = Game()
        self.games[game_id] = game


if __name__ == "__main__":
    man = Manager()
    man.create_game()
    print(man.games)
