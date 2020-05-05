import threading, queue
from database.db import get_all_creatures
from Systems.Resting import takeShortRest
from Systems.Combat import start_combat_handler
from Systems.log import setup_logging
from Systems.Creature import Creature
from time import sleep as time_sleep
TEST = 0

game_queue = queue.Queue()
logger = setup_logging()
all_creatures = []
class GameLoop:
    def __init__(self):
        self.current_time = 0

    def tick(self):
        self.current_time += 1
        print(f"Game is {self.current_time}")

def initalize_creatures():
    for creature in get_all_creatures():
        all_creatures.append(
            Creature(creature['name'], creature['level'], creature['experience'], creature['inventory'],
            creature['klasse'], creature['race'], creature['life'], creature['location'], creature['area'])
        )
    print(all_creatures)

def game_loop(Game, GameIsRunning):
    initalize_creatures()
    while GameIsRunning:
        Game.tick()
        while True:
            try:
                msg = game_queue.get_nowait()
            except queue.Empty:
                msg = {
                    "for":"sys",
                    "data":"Queue Empty or error fetching Queue"
                }
                break
        if msg["for"] == 'sys':
            print(msg["data"])
        if msg['for'] == 'combat':
            start_combat_handler(msg['data'], Game.current_time)
            pass
        takeShortRest("1", Game)
        time_sleep(1.0)

if __name__ == '__main__':
    game = GameLoop()
    game_loop(game, True)
