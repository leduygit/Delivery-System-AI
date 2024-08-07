import search_logic.solution as sol
from queue import PriorityQueue as p_queue


class BFS(sol.SolutionBase):  # Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def get_level(self):
        return "lv1"

    def solve(self):
        start, goal = self.agent_list[0]
        original_map = self.map_data.copy()

        queue = [(start, [start])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == goal:
                self.move_logs = self.trace_path(original_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])
            
            if current not in visited:
                visited.add(current)

                for neighbor, _ in self.graph.get_neighbors(current):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return "FAIL"


class DFS(sol.SolutionBase):  # Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def get_level(self):
        return "lv1"

    def solve(self):
        start, goal = self.agent_list[0]
        original_map = self.map_data.copy()


        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()

            if current == goal:
                self.move_logs = self.trace_path(original_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])

            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return "FAIL"


class UCS(sol.SolutionBase):  # Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def get_level(self):
        return "lv1"

    def solve(self):
        start, goal = self.agent_list[0]
        original_map = self.map_data.copy()
        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()

        while not queue.empty():
            cost, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(original_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])
            
            if current in visited:
                continue

            if current not in visited:
                visited.add(current)

                for neighbor, weight in self.graph.get_neighbors(current):
                    if neighbor not in visited:
                        if self.map_data[neighbor[0]][neighbor[1]] != 0:
                            weight += 1
                        queue.put((cost + weight, neighbor, path + [neighbor]))

        return "FAIL"


class GBFS(sol.SolutionBase):  # Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def get_level(self):
        return "lv1"


    # return the heuristic value of the current node
    def get_heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def solve(self):
        start, goal = self.agent_list[0]
        original_map = self.map_data.copy()


        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()

        while not queue.empty():
            _, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(original_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])

            if current in visited:
                continue
            
            visited.add(current)

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.put(
                        (
                            self.get_heuristic(neighbor, goal),
                            neighbor,
                            path + [neighbor],
                        )
                    )

        return "FAIL"


class Astar(sol.SolutionBase):  # Level 1
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def get_level(self):
        return "lv1"

    # return the heuristic value of the current node
    def get_heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def solve(self):
        start, goal = self.agent_list[0]
        original_map = self.map_data.copy()


        queue = p_queue()
        queue.put((0, start, [start]))
        visited = set()

        while not queue.empty():
            cost, current, path = queue.get()

            if current == goal:
                self.move_logs = self.trace_path(original_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])
            
            if current in visited:
                continue

            visited.add(current)

            cost -= self.get_heuristic(current, goal)

            for neighbor, weight in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.put(
                        (
                            cost + weight + self.get_heuristic(neighbor, goal),
                            neighbor,
                            path + [neighbor],
                        )
                    )

        return "FAIL"
