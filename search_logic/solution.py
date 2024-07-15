import json
import heapq

class SolutionBase:
    # storing problem data
    def __init__(self, graph, agent_list, gas=None):
        self.graph = graph
        self.agent_list = agent_list  # start, goal for each agent

        self.gas = gas
        self.move_logs = []  # Placeholder for move logs

    def trace_path(self, *args):
        raise NotImplementedError("Subclasses should implement the trace_path method")
    
    def get_heuristic(self, *args):
        raise NotImplementedError("Subclasses should implement the get_heuristic method")
    
    def solve(self):
        raise NotImplementedError("Subclasses should implement the solve method")
    
    def save_move_logs(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.move_logs, f)



class TestSolution(SolutionBase):
    def __init__(self, graph, agent_list, gas=None):
        super().__init__(graph, agent_list, gas)
    
    
    def get_heuristic(self, start, goal):
        # return the manhattan distance between start and goal
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    def solve(self):
        visited = set()
        frontier = []

        start, goal = self.agent_list[0]
        heapq.heappush(frontier, (0, start, [start]))

        while frontier:
            cost, current, path = heapq.heappop(frontier)

            if current == goal:
                self.move_logs.append(path)
                return path

            visited.add(current)

            for neighbor, weight in self.graph.get_neighbors(current):
                if neighbor not in visited and self.graph.get_nodes_values(neighbor) != '-1':
                    new_cost = cost + weight
                    new_path = path + [neighbor]
                    heapq.heappush(frontier, (new_cost + self.get_heuristic(neighbor, goal), neighbor, new_path))

        return None

#implement your solution here
class LevelSolution:
    pass