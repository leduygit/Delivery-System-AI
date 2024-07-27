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
    def __init__(self, agent_list, map, time, gas):
        super().__init__()
        self.time = time
        self.gas = gas
        self.map = map.copy()
        self.goals = [agent[1] for agent in agent_list]

    def bfsToGoal(self, map, state):
        # return the next move to reach the goal

        start = (state['x'], state['y'])
        goal = (state['goal_x'], state['goal_y'])
        time = state['time']
        initial_gas = state['gas']
        grid = map['grid']


        if start == goal:
            return None

        queue = pq()
        queue.put((0, time, start, initial_gas, []))
        visited = set()
        visited.add((start, time, initial_gas))
        prev = {}

        MARKER  = ['S', 'S1', 'S2', 'S3', 'S4', 'S5', 'S5', 'S6', 'S7', 'S7', 'S8', 'S9', 'S10']

        while not queue.empty():
            cost, time, current, current_gas, path = queue.get()
            if (start == (8 ,2) and state['time'] == 86):  
                print("Current state")
                print((current, time, current_gas))

            if current == goal:
                # return the next move from current to goal
                # print(path)
                print(path[0])
                return path[0]

            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for direction in directions:
                next_x = current[0] + direction[0]
                next_y = current[1] + direction[1]

                if next_x < 0 or next_x >= len(grid) or next_y < 0 or next_y >= len(grid[0]):
                    continue    

                # if isinstance(grid[next_x][next_y], str) and grid[next_x][next_y] in MARKER and grid[next_x][next_y] != grid[current[0]][current[1]]:
                #     # print(grid)
                #     continue

                if isinstance(self.map[next_x][next_y], int) and self.map[next_x][next_y] == -1:
                    continue                    

                map_value = get_value(self.map[next_x][next_y])
                new_time = time - 1 - get_value(map_value)
                new_gas = current_gas - 1

                if (type(self.map[next_x][next_y]) == tuple):
                    new_gas = self.gas
                    if (start == (8 ,2)):
                        print("GAS STATION")
                    #print(new_gas)

                if new_time < 0 or new_gas < 0:
                    continue

                if (next_x, next_y, new_time, new_gas) in visited:
                    continue

                visited.add((next_x, next_y, new_time, new_gas))
                prev[(next_x, next_y, new_time, new_gas)] = (current, direction)
                queue.put((cost + 1, new_time, (next_x, next_y), new_gas, path + [(next_x, next_y)]))

        # check if the bot is blocking the path of other bots
        # if so, move to a different cell
                
        

        return None
    
    def get_move(self, map, state):
        # return the next move for the agent
        next_move = self.bfsToGoal(map, state)
        return next_move
