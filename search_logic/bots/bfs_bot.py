from search_logic.bots.base import BotBase
from queue import PriorityQueue as pq


def get_value(value):
    if isinstance(value, tuple):
        return value[1]
    try:
        return int(value)
    except:
        return 0


class BfsBot(BotBase):
    def __init__(self, agent_list, map, time=None, gas=None):
        super().__init__()
        self.time = time
        self.gas = gas
        self.map = map
        self.goals = [agent[1] for agent in agent_list]

    def bfsToGoal(self, map, state):
        # return the next move to reach the goal

        start = (state['x'], state['y'])
        goal = (state['goal_x'], state['goal_y'])
        time = state['time']
        gas = state['gas']
        grid = map['grid']

        if start == goal:
            return None

        queue = pq()
        queue.put((0, time, start, gas, []))
        visited = set()
        visited.add((start, time, gas))
        prev = {}

        while not queue.empty():
            cost, time, current, current_gas, path = queue.get()

            if current == goal:
                # return the next move from current to goal
                # print(path)
                return path[0]

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for direction in directions:
                next_x = current[0] + direction[0]
                next_y = current[1] + direction[1]

                if next_x < 0 or next_x >= len(grid) or next_y < 0 or next_y >= len(grid[0]):
                    continue    

                if isinstance(grid[next_x][next_y], str) and grid[next_x][next_y][0] == 'S':
                    # print(grid)
                    continue

                if isinstance(grid[next_x][next_y], int) and grid[next_x][next_y] == -1:
                    continue

                map_value = get_value(grid[next_x][next_y])
                new_time = time - 1 - get_value(map_value)
                new_gas = current_gas - 1

                if new_time < 0 or new_gas < 0:
                    continue

                if (next_x, next_y, new_time, new_gas) in visited:
                    continue

                visited.add((next_x, next_y, new_time, new_gas))
                prev[(next_x, next_y, new_time, new_gas)] = (current, direction)
                queue.put((cost + 1, new_time, (next_x, next_y), new_gas, path + [(next_x, next_y)]))

        return None
    
    def get_move(self, map, state):
        # return the next move for the agent
        next_move = self.bfsToGoal(map, state)
        return next_move
