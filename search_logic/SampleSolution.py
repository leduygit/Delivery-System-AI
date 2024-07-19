import solution

class TestSolution(solution.SolutionBase):
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