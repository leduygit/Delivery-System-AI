class BotBase:
    def __init__(self):
        pass

    def get_move(self, map, state):
        raise NotImplementedError("Subclasses should implement the get_move method")
