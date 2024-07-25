import json


def cast_to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0


def parse_positions_file(filename):
    with open(filename, "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        positions = [[int(x) for x in line.split()] for line in lines]
    return positions


def get_waiting_time(map_data, position):
    waiting_time = map_data[position[0]][position[1]]
    if isinstance(waiting_time, tuple):
        return waiting_time[1]
    return waiting_time

def update_goal_positions(goal, agent_id, agent_list, map_data):
    agent_list[agent_id] = (agent_list[agent_id][1], goal)

    # erase previous path of the agent
    MARKERS = ["S", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]

    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell == MARKERS[agent_id]:
                map_data[i][j] = 0

    GOAL_MARKERS = ["G", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]

    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell == GOAL_MARKERS[agent_id]:
                map_data[i][j] = 0

    # update the new goal position
    goal_x, goal_y = goal
    map_data[goal_x][goal_y] = GOAL_MARKERS[agent_id]
    
    return agent_list, map_data



def create_json_output(map_data, agent_files, agent_list, initial_fuel=None, initial_time=None, agent_goal_list=None):
    MARKERS = ["S", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]  # Adjust the size based on the number of agents
    moves = []
    max_turns = 0
    agent_data = {}

    for i, file in enumerate(agent_files):
        agent_id = f"agent_{i+1}"
        positions = parse_positions_file(file)
        max_turns = max(max_turns, len(positions))
        agent_data[agent_id] = {
            "goal": agent_list[i][1],
            "path": positions,
            "fuel": initial_fuel,
            "time": initial_time,
            "reached": False,  # Track whether the agent has reached its goal
        }

    cumulative_positions = {agent_id: [] for agent_id in agent_data.keys()}
    cumulative_map = [row.copy() for row in map_data]

    total_time = initial_time if initial_time is not None else None
    for turn in range(max_turns):
        turn_data = {}

        for i, (agent_id, data) in enumerate(agent_data.items()):
            if turn < len(data["path"]):
                position = data["path"][turn]
            else:
                position = data["path"][-1]

            # Update cumulative positions
            cumulative_positions[agent_id].append(position)
            marker = MARKERS[i]  # Use marker from the constant array

            # Update the cumulative map with the agent's marker
            x, y = position
            cumulative_map[x][y] = marker

            # Calculate waiting time and total time
            waiting_time = get_waiting_time(map_data, position)
            waiting_time = cast_to_int(waiting_time)

            # Simulate time
            if total_time is not None:
                total_time -= waiting_time - 1
            else:
                total_time = None

            # Simulate fuel
            initial_fuel = data["fuel"]
            if initial_fuel is not None:
                fuel = max(0, initial_fuel - turn)
            else:
                fuel = None

            # Check if the agent has reached its goal
            if position == data["goal"]:
                data["reached"] = True

                # if the agent marker is not S, update the goal position this agent


            turn_data[agent_id] = {
                "position": position,
                "goal": data["goal"],
                "reached": data["reached"],
                "fuel": fuel,
                "time": total_time,
            }

        moves.append(
            {f"turn {turn}": turn_data, "map": [row.copy() for row in cumulative_map]}
        )

    return {"moves": moves}


def save_to_json(data, filename):
    """Save the data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
