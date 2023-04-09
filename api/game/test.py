from .Manager import Manager
from .models import Event, Player
import asyncio

man = Manager.get_instance()

async def scenario1():
    assert man is not None, "Manager can't be none"
    """
    Alice creates a game
    Bob connects to a new game.
    """
    create_event = Event(action="CREATE", nickname="Alice")
    await man.dispatch(create_event)

    gid = list(man.games.keys())[0]
    for _ in range(10):
        join_event = Event(action="JOIN", nickname="Bob", game_id=gid)
        await man.dispatch(join_event)


    other_action = Event(action="START", nickname="Alice", player_id=0, game_id=gid)
    await man.dispatch(other_action)

    # print(man.games[gid].players)



if __name__ == "__main__":
    asyncio.run(scenario1())
