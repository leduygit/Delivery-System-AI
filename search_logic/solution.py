import json

def get_value(value):
    if isinstance(value, tuple):
        return value[1]
    
    try:
        return int(value)
    except:
        return 0


class SolutionBase:
    # storing problem data
    def __init__(self, graph, agent_list, map_data, time=None, gas=None):
        self.graph = graph
        self.agent_list = agent_list  # start, goal for each agent
        self.map_data = map_data
        self.time = time
        self.gas = gas
        self.time = time
        self.move_logs = []  # Placeholder for move logs

    
    def trace_path(self, map, path):
        move_logs = []
        #print(self.get_level())
        for i in range(len(path)):
            #print("trace_path")
            #print(i)
            ##print(path[i][0], path[i][1])
            value = get_value(map[path[i][0]][path[i][1]])
            while value >= 0:
                move_logs.append((path[i]))
                value -= 1
        #print(move_logs)
        return move_logs

    def get_level(self):
        raise NotImplementedError("Subclasses should implement the get_level method")

    def solve(self):
        raise NotImplementedError("Subclasses should implement the solve method")

    def save_move_logs(self, filename):
        with open(filename, "w") as file:
            if len(self.move_logs) == 0:
                start, _ = self.agent_list[0]
                file.write(f"{start[0]} {start[1]}")
            else:
                file.write("\n".join([f"{x} {y}" for x, y in self.move_logs]))
