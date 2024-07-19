import json
import graph

class SolutionBase:
    # storing problem data
    def __init__(self, graph, agent_list, map_data, time=None, gas=None):
        self.graph = graph
        self.agent_list = agent_list  # start, goal for each agent
        self.map_data = map_data
        self.time = time
        self.gas = gas
        self.move_logs = []  # Placeholder for move logs

    def trace_path(self, *args):
        raise NotImplementedError("Subclasses should implement the trace_path method")
    
    def solve(self):
        raise NotImplementedError("Subclasses should implement the solve method")
    
    def save_move_logs(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.move_logs, f)



class TestSolution(SolutionBase):
    def __init__(self, graph, agent_list, map_data, gas=None):
        super().__init__(graph, agent_list, map_data, gas)

    def trace_path(self, path):
        move_logs = []
        for i in range(len(path)):
            move_logs.append((path[i]))
        return move_logs

    def solve(self):
        # bfs from start to goal
        start, goal = self.agent_list[0]

        queue = [(start, [start])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
    
            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return 'FAIL'

#implement your solution here
class LevelSolution:
    pass