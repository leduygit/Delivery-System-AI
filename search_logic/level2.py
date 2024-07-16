import solution as sol
from queue import PriorityQueue as p_queue

class TimeLimitLevel(sol.SolutionBase): #level 2
    def __init__(self, graph, agent_list, map_data, time=None):
        super().__init__(graph, agent_list, map_data, time)
        self.heuristic = self.generate_heuristic(agent_list[0][1])
        
    def trace_path(self, path):
        move_logs = []
        for i in range(len(path)):
            move_logs.append((path[i]))
        return move_logs
    
    def generate_heuristic(self, goal): # Manhattan distance
        rows, cols = len(self.map_data), len(self.map_data[0])
        heuristics = {}

        for r in range(rows):
            for c in range(cols):
                if self.map_data[r][c] == -1:
                    heuristics[(r, c)] = 1000000
                else:
                    heuristics[(r, c)] = abs(r - goal[0]) + abs(c - goal[1]) + self.map_data[r][c]

        return heuristics
        
    #shortest path under time limit 
    def solve(self):
        start, goal = self.agent_list[0]
        
        queue = p_queue()
        queue.put((0, 0, start, [start]))
        visited = set()
        
        while not queue.empty():
            _, cost, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
            
            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    ncost = cost + 1 + self.map_data[neighbor[0]][neighbor[1]]
                    queue.put((self.heuristic[neighbor], ncost, neighbor, path + [neighbor]))
    
        return 'FAIL'
