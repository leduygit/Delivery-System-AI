import solution as sol
from queue import PriorityQueue as p_queue

class BasicLevel(sol.SolutionBase): #Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)
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
                heuristics[(r, c)] = abs(r - goal[0]) + abs(c - goal[1])

        return heuristics
    
    #Search Strategies
    def BFS(self):
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
    
    
    def DFS(self):
        start, goal = self.agent_list[0]
        
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            current, path = stack.pop()

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
            
            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
        return 'FAIL'
    
    
    def UCS(self):
        start, goal = self.agent_list[0]
        
        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()
        
        while not queue.empty():
            cost, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
            
            visited.add(current)

            for neighbor, weight in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.put((cost + weight, neighbor, path + [neighbor]))
    
        return 'FAIL'
    
    
    def GBFS(self):
        start, goal = self.agent_list[0]
        
        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()
        
        while not queue.empty():
            _, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
            
            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.put((self.heuristic[neighbor], neighbor, path + [neighbor]))
    
        return 'FAIL'
    
    
    def Astar(self):
        start, goal = self.agent_list[0]
        
        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()
        
        while not queue.empty():
            cost, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
            
            visited.add(current)
            
            cost -= self.heuristic[current]

            for neighbor, weight in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.put((cost + weight + self.heuristic[neighbor], neighbor, path + [neighbor]))
    
        return 'FAIL'
    
    