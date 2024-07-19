import json

def cast_to_int(value):
    """Attempt to cast a value to an integer, returning 0 if conversion fails."""
    try:
        return int(value)
    except ValueError:
        return 0

def parse_positions_file(filename):
    """Parse a single text file to extract the list of positions."""
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        positions = [[int(x) for x in line.split()] for line in lines]
    return positions

def get_waiting_time(map_data, position):
    """Return the waiting time for a given position from the map."""
    return map_data[position[0]][position[1]]

def create_json_output(map_data, agent_files, initial_fuel = None, initial_time = None):
    """Create a JSON output with paths from multiple agent files, simulating fuel and time."""
    moves = []
    max_turns = 0
    agent_data = {}

    # Parse each agent file
    for i, file in enumerate(agent_files):
        agent_id = f"agent_{i+1}"
        positions = parse_positions_file(file)
        max_turns = max(max_turns, len(positions))
        agent_data[agent_id] = {
            "goal": positions[-1],
            "path": positions,
            "fuel": initial_fuel,
            "time": initial_time,
        }

    # Generate moves for each turn
    total_time = initial_time if initial_time is not None else None
    for turn in range(max_turns):
        turn_data = {}
        for agent_id, data in agent_data.items():
            if turn < len(data["path"]):
                position = data["path"][turn]
            else:
                position = data["path"][-1]  # Stay at the last position if beyond path length

            # Calculate waiting time and total time
            waiting_time = get_waiting_time(map_data, position)
            waiting_time = cast_to_int(waiting_time)  # Ensure waiting_time is an integer

            
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
                fuel = None  # Keep fuel as None if not provided

            turn_data[agent_id] = {
                "position": position,
                "goal": data["goal"],
                "reached": position == data["goal"],
                "fuel": fuel,
                "time": total_time
            }

        moves.append({f"turn {turn}": turn_data})

    return {"map": map_data, "moves": moves}

def save_to_json(data, filename):
    """Save the data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
