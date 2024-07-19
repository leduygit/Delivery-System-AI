import json
from collections import deque

class SolutionBase:
    def __init__(self, graph, agent_list, map_data, time=None, gas=None, log_file=None):
        self.graph = graph
        self.agent_list = agent_list  # list of tuples: (start, goal) for each agent
        self.map_data = map_data
        self.time = time
        self.gas = gas
        self.move_logs = {
            "map": map_data,
            "moves": {}  # Each move will be added here with detailed agent info, keyed by turn number
        }
        self.log_file = log_file  # File path to store move logs

    def add_move(self, turn, agents_positions):
        """
        Add a move for a specific turn.

        Parameters:
        turn (int): The turn number.
        agents_positions (list): A list of agent positions for the current turn.
        """
        agents_state = self.generate_agents_state(agents_positions)
        self.move_logs["moves"][f"turn {turn}"] = agents_state

    def generate_agents_state(self, agents_positions):
        """
        Generate the state of each agent.

        Parameters:
        agents_positions (list): A list of agent positions.

        Returns:
        dict: A dictionary with agent IDs as keys and their states as values.
        """
        agents_state = {}
        for i, (agent_start, agent_goal) in enumerate(self.agent_list):
            position = agents_positions[i]
            reached_goal = position == agent_goal
            agent_state = {
                "position": position,
                "goal": agent_goal,
                "reached_goal": reached_goal
            }
            agents_state[f"agent_{i+1}"] = agent_state
        return agents_state

    def trace_path(self, *args):
        raise NotImplementedError("Subclasses should implement the trace_path method")

    def solve(self):
        raise NotImplementedError("Subclasses should implement the solve method")

    def save_move_logs(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.move_logs, f, indent=2)

class TestSolution(SolutionBase):
    def __init__(self, graph, agent_list, map_data, gas=None):
        super().__init__(graph, agent_list, map_data, gas)

    def bfs(self, start, goal):
        queue = deque([(start, [start])])
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            for neighbor, _ in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []  # Return empty path if no path is found

    def trace_path(self, agent_paths):
        max_turns = max(len(path) for path in agent_paths)
        for turn in range(max_turns):
            current_positions = [
                path[turn] if turn < len(path) else path[-1] for path in agent_paths
            ]
            self.add_move(turn + 1, current_positions)

    def solve(self):
        print(f"Agent list: {self.agent_list}")  # Debug print
        agent_paths = [self.bfs(start, goal) for start, goal in self.agent_list]
        self.trace_path(agent_paths)

