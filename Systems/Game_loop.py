import threading, queue
from database.db import get_all_creatures, preload
from database.db import session
from web.web import webSession
from Systems.Resting import takeShortRest
from Systems.Combat import start_combat_handler
from Systems.log import setup_logging
from Systems.Creature import CCreature
from time import sleep as time_sleep
TEST = 0

game_queue = queue.SimpleQueue()
logger = setup_logging()
all_creatures = []
preload(session)
class GameLoop:
    def __init__(self):
        self.current_time = 0

    def tick(self):
        self.current_time += 1
        print(f"Game is {self.current_time}")



def initalize_creatures():
    for a_creature in get_all_creatures():
        crr = CCreature(a_creature.name, a_creature.level, a_creature.experience, a_creature.inventory,
            a_creature.klasse, a_creature.race, a_creature.life, a_creature.location, a_creature.area)
        all_creatures.append(crr)
        game_queue.put({
            "for":"sys",
            "data":"All creatures initalized, areas next."
        })

def game_loop(Game, GameIsRunning):
    www = threading.Thread(target=webSession, args=(session, game_queue), daemon=True)
    www.start()
    initalize_creatures()
    while GameIsRunning:
        Game.tick()
        while True:
            print("Getting queue")
            try:
                msg = game_queue.get_nowait()
            except queue.Empty:
                break
        print(msg)
        if msg["for"] == 'sys':
            print(msg["data"])
        if msg['for'] == 'combat':
            #start_combat_handler(msg['data'], Game.current_time)
            pass

        if msg['for'] == 'creatures':
            print("GETTING ALL CREATURES")
            creatures = get_all_creatures()
            game_queue.put({
                "for":"web_creatures",
                "data":creatures
            })
        #takeShortRest("1", Game)
        time_sleep(1.0)

if __name__ == '__main__':
    game = GameLoop()
    game_loop(game, True)
