import solution
from collections import deque
import heapq

class TestSolution(solution.SolutionBase):
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def initialize_state_list(self):
        return deque()

    def get_top_state(self):
        if self.state_list:
            return self.state_list.popleft()
        return None

    def add_next_state_to_list(self, next_state):
        self.state_list.append(next_state)


class HeapSolution(solution.SolutionBase):
    def __init__(self, graph, agent_list, map_data):
        super().__init__(graph, agent_list, map_data)

    def initialize_state_list(self):
        return []

    def get_heuristic(self, state):
        # sum of manhattan distances of all agents to their goals
        heuristic_value = 0
        for agent in state["agents"]:
            heuristic_value += abs(agent["position"][0] - agent["goal"][0]) + abs(agent["position"][1] - agent["goal"][1])

        return heuristic_value

    def add_next_state_to_list(self, next_state):
        state_key = self.state_to_key(next_state)
        new_cost = next_state["cost"]
        self.state_costs[state_key] = new_cost
        heapq.heappush(self.state_list, (new_cost + self.get_heuristic(next_state), state_key, next_state))

    def get_top_state(self):
        if self.state_list:
            _, _, state = heapq.heappop(self.state_list)
            return state
        return None