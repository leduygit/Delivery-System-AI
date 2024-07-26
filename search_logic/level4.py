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

def is_valid_move(grid, state, move):
    ox, oy = state['x'], state['y']
    nx, ny = move
    grid = grid['grid']
    return 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and \
           grid[nx][ny] != -1 and abs(nx - ox) + abs(ny - oy) == 1 \
           and state['gas'] > 0 and state['time'] > 0

def apply_moves(map, state, move, index):
    cur_x, cur_y = state['x'], state['y']
    goal = (state['goal_x'], state['goal_y'])
    grid = map['grid']
    grid[cur_x][cur_y] = '.'
    if move == goal:
        state['goal_x'], state['goal_y'] = get_new_goal(grid, (cur_x, cur_y))
    if isinstance(grid[move[0]][move[1]], tuple) and grid[move[0]][move[1]].startswith('F'):
        state['gas'] = map['gas']
        state['wait'] = int(grid[move[0]][move[1]][1])
    else:
        state['gas'] -= 1

    if isinstance(grid[move[0]][move[1]], int):
        state['wait'] = grid[move[0]][move[1]]
    
    state['time'] -= 1
    state['x'], state['y'] = move
    grid[move[0]][move[1]] = 'S{}'.format(index + 1)
    return grid, state


def print_current(states):
    for i, _ in enumerate(states):
        pos = (states[i]['x'], states[i]['y'])
        with open('search_logic/agents/agent_{}.txt'.format(i + 1), 'a') as f:
            f.write('{} {}\n'.format(pos[0], pos[1]))

        goal = (states[i]['goal_x'], states[i]['goal_y'])
        with open('search_logic/agents/goal_{}.txt'.format(i + 1), 'a') as f:
            f.write('{} {}\n'.format(goal[0], goal[1]))


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
        'grid': grid,
        'height': len(grid),
        'width': len(grid[0]),
        'gas': gas,
    }

    current_positions = [pos[0] for pos in start_positions]
    current_goals = [pos[1] for pos in start_positions]

    # Initialize bots with the starting gas and time for each agent
    bots = [bfs_bot(grid, time, gas) for _ in current_positions]
    states = []
    for i, bot in enumerate(bots):
        states.append({
            'x': current_positions[i][0],
            'y': current_positions[i][1],
            'goal_x': current_goals[i][0],
            'goal_y': current_goals[i][1],
            'gas': gas,
            'time': time,
            'wait': 0,
        })

    for i, bot in enumerate(bots):
        with open("search_logic/agents/agent_{}.txt".format(i + 1), "w") as f:
            f.write("")
        with open("search_logic/agents/goal_{}.txt".format(i + 1), "w") as f:
            f.write("")

    agent_current_fuel = [gas for _ in current_positions]
    agent_current_time = [time for _ in current_positions]

    while time > 0:
        for i, bot in enumerate(bots):
            move = bot.get_move(mmap, states[i])
            print(move)
            if move is None or not is_valid_move(mmap, states[i], move) or states[i]['wait'] > 0:
                states[i]['wait'] -= states[i]['wait'] > 0
                print_current(states)
                continue
            mmap['grid'], states[i] = apply_moves(mmap, states[i], move, i)
            print_current(states)
        time -= 1

    input_files = [f"search_logic/agents/agent_{i+1}.txt" for i in range(len(bots))]
    output_file = "Assets/Json/lv4/output.json"

    # Create JSON output data
    data = fo.create_json_output(copy_grid, input_files, start_positions, gas, time)
    # Save JSON to file
    fo.save_to_json(data, output_file)
