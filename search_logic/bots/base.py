class BotBase:
    def __init__(self, *args):
        pass

    def get_move(self, map, state, current_pos):
        raise NotImplementedError("Subclasses should implement the get_move method")
