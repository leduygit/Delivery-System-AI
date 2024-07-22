import json

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

    def get_level(self):
        raise NotImplementedError("Subclasses should implement the get_level method")

    def trace_path(self, *args):
        raise NotImplementedError("Subclasses should implement the trace_path method")
    
    def solve(self):
        raise NotImplementedError("Subclasses should implement the solve method")
    
    def save_move_logs(self, filename):
        with open(filename, 'w') as file:
            file.write('\n'.join([f'{x} {y}' for x, y in self.move_logs]))

