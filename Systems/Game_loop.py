import threading, queue
from Systems.Resting import takeShortRest
from Systems.log import setup_logging
from time import sleep as time_sleep
TEST = 0

game_queue = queue.Queue()
logger = setup_logging()

class GameLoop:
    def __init__(self):
        self.current_time = 0

    def tick(self):
        self.current_time += 1


def game_loop(Game, GameIsRunning):
    while GameIsRunning:
        Game.tick()
        while True:
            try:
                msg = game_queue.get_nowait()
            except queue.Empty:
                msg = {
                    "for":"sys",
                    "data":"Error fetching Queue"
                }
                break
        if msg["for"] == 'sys':
            print(msg["data"])

        takeShortRest("1", Game)
        time_sleep(1.0)

if __name__ == '__main__':
    game = GameLoop()
    game_loop(game, True)
