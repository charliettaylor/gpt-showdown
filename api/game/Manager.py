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

        self.games = [1, 2, 3]

    def get_games(self):
        return self.games

    def add_game(self, to_add: int):
        self.games.append(4)


if __name__ == "__main__":
    man = Manager()
    man2 = Manager.get_instance() or man
    man.add_game(4)
    print(man.get_games())
    print(man2.get_games())
