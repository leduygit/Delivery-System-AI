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

def parse_goal_file(filename):
    with open(filename, "r") as file:
        # read all lines
        lines = [line.strip() for line in file if line.strip()]
        # parse each line into a tuple of integers
        goals = [(int(x), int(y)) for line in lines for x, y in [line.split()]]
    return goals


def get_waiting_time(map_data, position):
    waiting_time = map_data[position[0]][position[1]]
    if isinstance(waiting_time, tuple):
        return waiting_time[1]
    return waiting_time

def update_goal_positions(goal, agent_id, agent_list, map_data):
    agent_list[agent_id] = (agent_list[agent_id][1], goal)

    # Erase previous path of the agent
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

    # Update the new goal position
    goal_x, goal_y = goal
    map_data[goal_x][goal_y] = GOAL_MARKERS[agent_id]

    return agent_list, map_data

def update_map(map_data, agent_id, new_goal, current_position, original_map):
    # Erase previous path of the agent

    MARKERS = ["S", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    GOAL_MARKERS = ["G", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]

    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if (cell == MARKERS[agent_id] or  cell == GOAL_MARKERS[agent_id]) and (i, j) != current_position:
                if original_map[i][j] == MARKERS[agent_id] or original_map[i][j] == GOAL_MARKERS[agent_id]:
                    map_data[i][j] = 0
                else:
                    map_data[i][j] = original_map[i][j]

    # Update the new goal position
    map_data[current_position[0]][current_position[1]] = MARKERS[agent_id]
                
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if (i, j) == new_goal:
                map_data[i][j] = GOAL_MARKERS[agent_id]

    return map_data

    

def create_json_output(
    map_data,
    agent_files,
    agent_goal_files,
    agent_list,
    initial_fuel=None,
    initial_time=None
):
    MARKERS = ["S", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    moves = []
    max_turns = 0
    agent_data = {}
    goal_list = [[] for _ in range(len(agent_files))]
    original_map = [row.copy() for row in map_data]

    for i, agent_file in enumerate(agent_files):
        agent_id = f"agent_{i+1}"
        positions = parse_positions_file(agent_file)
        max_turns = max(max_turns, len(positions))
        if agent_goal_files[i] is not None:
            goal = parse_goal_file(agent_goal_files[i])
            #print(agent_goal_files[i])
            goal_list[i] = goal
        else:
            goal = agent_list[i][1]  # Use the goal from agent_list if goal file is None
        agent_data[agent_id] = {
            "goal": goal,
            "path": positions,
            "fuel": initial_fuel,
            "time": initial_time,
            "reached": False,
        }

    # print goal list

    cumulative_positions = {agent_id: [] for agent_id in agent_data.keys()}
    cumulative_map = [row.copy() for row in map_data]

    total_time = initial_time if initial_time is not None else None
    for turn in range(max_turns):
        turn_data = {}

        # update new goal positions


        for i, (agent_id, data) in enumerate(agent_data.items()):
            if turn < len(data["path"]):
                position = data["path"][turn]
            else:
                position = data["path"][-1]

            # Update cumulative positions
            cumulative_positions[agent_id].append(position)
            marker = MARKERS[i]

            # Update the cumulative map with the agent's marker
            x, y = position
            cumulative_map[x][y] = marker

            # Calculate waiting time and total time
            waiting_time = get_waiting_time(map_data, position)
            waiting_time = cast_to_int(waiting_time)

            # Simulate time
            if (data["time"] is not None and turn > 0):
                data["time"] -= 1
            

            # Simulate fuel
            initial_fuel = data["fuel"]
            if initial_fuel is not None:
                # if move to another cell
                if turn > 0 and position != data["path"][turn-1]:
                    data["fuel"] -= 1

            # Check if the agent has reached its goal
            if position == data["goal"]:
                data["reached"] = True

            # print goal[i][turn] if turn < len(goal[i]) else data["goal"]
            #print(goal_list[i])
            #print(f"Agent {agent_id} at {position} with goal {goal_list[i][turn] if turn < len(goal_list[i]) else data['goal']}")
                
            # if the goal is updated, update the map


            turn_data[agent_id] = {
                "position": position,
                "goal": goal_list[i][turn] if turn < len(goal_list[i]) else data["goal"],
                "fuel": data["fuel"],
                "time": data["time"],
                "reached": data["reached"],
            }

            if (turn > 1):
                if (turn < len(goal_list[i]) and goal_list[i][turn] != goal_list[i][turn-1]):
                    cumulative_map = update_map(cumulative_map, i, goal_list[i][turn], position, original_map)

        moves.append(
            {f"turn {turn}": turn_data, "map": [row.copy() for row in cumulative_map]}
        )

    return {"moves": moves}

def save_to_json(data, filename):
    """Save the data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
