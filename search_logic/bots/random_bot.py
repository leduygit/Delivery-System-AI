from random import randint
from search_logic.bots.base import BotBase


class RandomBot(BotBase):
    def __init__(self):
        super().__init__()

    def get_move(self, map, state):
        dx = randint(-1, 1)
        dy = randint(-1, 1)

        return state['x'] + dx, state['y'] + dy