import json

class SolutionBase:
    def __init__(self, graph, agent_list, map_data, gas=None, time=None):
        self.graph = graph
        self.agent_list = agent_list
        self.data = {
            "map": map_data,
            "moves": []
        }
        self.turn = 0
        self.state_list = self.initialize_state_list()
        self.agents_state = [
            {
                "position": start,
                "goal": goal,
                "reached": start == goal,
                "path": [start]
            } for start, goal in agent_list
        ]
        self.gas = gas
        self.time = time
        self.visited_states = set()
        self.state_costs = {}  # Dictionary to track the minimum cost for each state

    def agent_state(self, position, goal, reached):
        return {
            "position": position,
            "goal": goal,
            "reached": reached
        }
    
    def is_goal_state(self, state):
        return all(agent["reached"] for agent in state["agents"])

    def log_move(self, state):
        turn_log = {f"turn {self.turn}": {}}
        for i, agent in enumerate(state["agents"]):
            turn_log[f"turn {self.turn}"][f"agent_{i+1}"] = {
                "position": agent["position"],
                "goal": agent["goal"]
            }
        self.data["moves"].append(turn_log)
        self.turn += 1

    def generate_next_state(self, chosen_agent_index, current_state):
        agent = current_state["agents"][chosen_agent_index]
        agent_position = agent["position"]
        current_turn = current_state["turn"]

        next_states = []
        if not agent["reached"]:
            for neighbor, weight in self.graph.get_neighbors(agent_position):
                next_agents_state = current_state["agents"][:]
                next_agents_state[chosen_agent_index] = {
                    "position": neighbor,
                    "goal": agent["goal"],
                    "reached": neighbor == agent["goal"],
                    "path": agent["path"] + [neighbor]
                }
                next_states.append({
                    "turn": current_turn + 1,
                    "cost": current_state["cost"] + weight,
                    "agents": next_agents_state,
                    "parent": current_state
                })
        return next_states
    
    def get_heuristic(self, state):
        # Calculate heuristic value (Manhattan distance)
        heuristic_value = 0
        for agent in state["agents"]:
            heuristic_value += abs(agent["position"][0] - agent["goal"][0]) + abs(agent["position"][1] - agent["goal"][1])
        return heuristic_value
    
    def initialize_state_list(self):
        """Initialize the state list. Subclasses should override this to use different data structures."""
        raise NotImplementedError("Subclasses should implement the initialize_state_list method")
    
    def get_top_state(self):
        """Get the top state from the state list. Subclasses should override this to use different data structures."""
        raise NotImplementedError("Subclasses should implement the get_top_state method")
    
    def add_next_state_to_list(self, next_state):
        """Add the next state to the state list. Subclasses should override this to use different data structures."""
        raise NotImplementedError("Subclasses should implement the add_next_state_to_list method")
    
    def is_valid_state(self, state):
        state_key = self.state_to_key(state)

        # Check if already visited
        if state_key in self.visited_states:
            return False

        # No agent should be in the same position
        positions = [agent["position"] for agent in state["agents"]]
        if len(positions) != len(set(positions)):
            return False

        if state_key not in self.state_costs:
            self.state_costs[state_key] = float('inf')

        new_cost = state["cost"]

        if new_cost < self.state_costs[state_key]:
            self.state_costs[state_key] = new_cost
            return True
        return False
    
    def update_parent_state(self, state, parent_state):
        state["parent"] = parent_state

    def get_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.get("parent")
        return path[::-1]
    
    def solve(self):
        # Initialize state list with initial state
        initial_state = {"turn": 0, "cost": 0, "agents": self.agents_state, "parent": None}
        self.add_next_state_to_list(initial_state)
        self.state_costs[self.state_to_key(initial_state)] = 0

        loop_count = 0

        while self.state_list_not_empty() and loop_count < 1000000:
            top_state = self.get_top_state()

            if self.is_goal_state(top_state):
                solution_path = self.get_path(top_state)
                for state in solution_path:
                    self.agents_state = state["agents"]
                    self.log_move(state)
                return solution_path
            
            self.visited_states.add(self.state_to_key(top_state))

            current_turn = top_state["turn"]
            #print(f"Turn: {current_turn}")
            current_agents_state = top_state["agents"]

            chosen_agent_index = current_turn % len(current_agents_state)

            next_states = self.generate_next_state(chosen_agent_index, top_state)

            not_move = True
            for state in next_states:
                if self.is_valid_state(state):
                    # if (current_turn == 0):
                    #     print("State is valid")
                    #     print(state)
                    not_move = False
                    self.add_next_state_to_list(state)
                    self.update_parent_state(state, top_state)

            if not_move:
                top_state["turn"] += 1
                self.add_next_state_to_list(top_state)

            loop_count += 1
    
    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)
    
    def state_to_key(self, state):
        return tuple(agent["position"] for agent in state["agents"]), state["turn"]
    
    def state_list_not_empty(self):
        return len(self.state_list) > 0




