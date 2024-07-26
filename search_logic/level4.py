import os
from random import randint
from search_logic.bots.bfs_bot import BfsBot as bfs_bot
from search_logic.main import load_data
import search_logic.format_output as fo
import search_logic.graph as graph


def get_value(value):
    if isinstance(value, tuple):
        return ("F", value[1])
    try:
        return int(value)
    except:
        return 0


def is_valid_move(grid, ox, oy, nx, ny):
    return (
        0 <= nx < len(grid)
        and 0 <= ny < len(grid[0])
        and grid[nx][ny] != -1
        and abs(nx - ox) + abs(ny - oy) == 1
    )


def apply_moves(grid, start_position, move, index):
    grid[start_position[0]][start_position[1]] = "."
    grid[move[0]][move[1]] = "S{}".format(index + 1)
    return grid


def print_current(positions, goals):
    for i, pos in enumerate(positions):
        with open("search_logic/agents/agent_{}.txt".format(i + 1), "a") as f:
            f.write("{} {}\n".format(pos[0], pos[1]))

    for i, goal in enumerate(goals):
        with open("search_logic/agents/goal_{}.txt".format(i + 1), "a") as f:
            f.write("{} {}\n".format(goal[0], goal[1]))


def get_new_goal(grid, current_position):
    places = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ".":
                places.append((i, j))

    if not places:
        return current_position
    index = randint(0, len(places) - 1)
    return places[index]


def runner():
    grid, start_positions, time, gas = load_data("search_logic/input4.txt")
    g = graph.GridGraph(grid)

    copy_grid = [list(row) for row in grid]
    os.makedirs("search_logic/agents", exist_ok=True)
    mmap = {
        "grid": grid,
        "height": len(grid),
        "width": len(grid[0]),
    }

    current_positions = [pos[0] for pos in start_positions]
    current_goals = [pos[1] for pos in start_positions]

    # Initialize bots with the starting gas and time for each agent
    bots = [bfs_bot(grid, time, gas) for _ in current_positions]

    for i, bot in enumerate(bots):
        with open("search_logic/agents/agent_{}.txt".format(i + 1), "w") as f:
            f.write("")
        with open("search_logic/agents/goal_{}.txt".format(i + 1), "w") as f:
            f.write("")

    agent_current_fuel = [gas for _ in current_positions]
    agent_current_time = [time for _ in current_positions]

    while time > 0:
        for i, bot in enumerate(bots):
            state = {
                "x": current_positions[i][0],
                "y": current_positions[i][1],
                "goal_x": current_goals[i][0],
                "goal_y": current_goals[i][1],
                "time": agent_current_time[i],
                "gas": agent_current_fuel[i],
                "agent_id": i,
            }
            move = bot.get_move(mmap, state, current_positions)
            # print(move)
            if move is None or not is_valid_move(
                mmap["grid"],
                current_positions[i][0],
                current_positions[i][1],
                move[0],
                move[1],
            ):
                print_current(current_positions, current_goals)
                continue

            # Update the grid and agent positions
            mmap["grid"] = apply_moves(mmap["grid"], current_positions[i], move, i)
            current_positions[i] = move

            # Update time and gas for each agent

            # if new position is a gas station, refill gas
            grid_value = get_value(grid[move[0]][move[1]])

            if type(grid_value) == tuple and grid_value[0] == "F":
                agent_current_fuel[i] = gas
                agent_current_time[i] -= 1
            else:
                # if the agent is moving to another cell, decrement gas
                if (move[0], move[1]) != current_positions[i]:
                    agent_current_fuel[i] -= 1
                agent_current_time[i] -= 1 - grid_value

            # Update the bot with new time and gas values
            bots[i].time = state["time"]
            bots[i].gas = state["gas"]

            print_current(current_positions, current_goals)

        time -= 1

    input_files = [f"search_logic/agents/agent_{i+1}.txt" for i in range(len(bots))]
    output_file = "Assets/Json/lv4/output.json"

    # Create JSON output data
    data = fo.create_json_output(copy_grid, input_files, start_positions, gas, time)
    # Save JSON to file
    fo.save_to_json(data, output_file)
