import os
from random import randint
from search_logic.bots.bfs_bot import BfsBot as bfs_bot
from search_logic.logic import load_data
import search_logic.format_output as fo
import search_logic.graph as graph


def get_value(value):
    if isinstance(value, tuple):
        return ("F", value[1])
    try:
        return int(value)
    except:
        return 0

def is_valid_move(map, state, move):
    ox, oy = state['x'], state['y']
    nx, ny = move
    grid = map['grid']
    return 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and \
           grid[nx][ny] != -1 and abs(nx - ox) + abs(ny - oy) == 1 \
           and state['gas'] > 0 and state['time'] > 0

def apply_moves(map, state, move, index, original_state, current_positions):
    cur_x, cur_y = state['x'], state['y']
    goal = (state['goal_x'], state['goal_y'])
    grid = map['grid']
    if move == goal:
        if index == 0:
            state['x'], state['y'] = move
            return grid, state
        state['goal_x'], state['goal_y'] = get_new_goal(grid, (cur_x, cur_y))

    x, y = move
    if isinstance(original_state["map"][x][y], tuple):
        #print("REFUELING", x, y)
        state['gas'] = original_state["gas"]
        state['wait'] = original_state["map"][x][y][1]
    else:
        # if move to another cell then reduce gas
        if move != (cur_x, cur_y):
            state['gas'] -= 1

    if isinstance(original_state["map"][x][y], int):
        if state['wait'] > 0:
            raise ValueError("Error: Agent is waiting")
        state['wait'] = original_state["map"][x][y]
    


    state['time'] -= 1 
    state['x'], state['y'] = move
    if map['sgrid'][cur_x][cur_y] == 'S{}'.format(index) or map['sgrid'][cur_x][cur_y] == 'S':
        grid[cur_x][cur_y] = 0
    else:
        grid[cur_x][cur_y] = map['sgrid'][cur_x][cur_y]
    grid[move[0]][move[1]] = 'S{}'.format(index)
    #print(state)
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
            if grid[i][j] == 0:
                places.append((i, j))

    if not places:
        return current_position
    index = randint(0, len(places) - 1)
    return places[index]

def runner(filename):
    grid, start_positions, time, gas = load_data(filename)
    initial_time = time
    g = graph.GridGraph(grid)

    copy_grid = [list(row) for row in grid]
    os.makedirs("search_logic/agents", exist_ok=True)
    mmap = {
        'sgrid': grid,
        'grid': grid,
        'height': len(grid),
        'width': len(grid[0]),
        'gas': gas,
    }

    current_positions = [pos[0] for pos in start_positions]
    current_goals = [pos[1] for pos in start_positions]




    # Initialize bots with the starting gas and time for each agent
    bots = [bfs_bot(start_positions, copy_grid, time, gas) for _ in current_positions]
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

    original_state = {
        'map': copy_grid,
        'gas': gas,
    }
    

    for i, bot in enumerate(bots):
        with open("search_logic/agents/agent_{}.txt".format(i + 1), "w") as f:
            f.write("")
        with open("search_logic/agents/goal_{}.txt".format(i + 1), "w") as f:
            f.write("")

    print_current(states)
    done = False
    while time > 0 and not done:
        for i, bot in enumerate(bots):
            if states[i]['wait'] > 0:
                states[i]['wait'] -= 1
                states[i]['time'] -= 1
                print_current(states)
                continue
            move = bot.get_move(mmap, states[i], current_positions)
            #print(move)

            if move in current_positions and grid[move[0]][move[1]] != 'S{}'.format(i):
                states[i]['time'] -= 1
                print_current(states)
                continue
            if move is None:
                states[i]['time'] -= 1
                print_current(states)
                continue
            mmap['grid'], states[i] = apply_moves(mmap, states[i], move, i, original_state, current_positions)
            print_current(states)
            if i == 0 and states[i]['x'] == states[i]['goal_x'] and states[i]['y'] == states[i]['goal_y']:
                done = True
                break
            current_positions[i] = (states[i]['x'], states[i]['y'])
        time -= 1

    input_files = [f"search_logic/agents/agent_{i+1}.txt" for i in range(len(bots))]
    goal_files = [f"search_logic/agents/goal_{i+1}.txt" for i in range(len(bots))]
    output_file = filename.replace("Maps", "Json").replace(".txt", ".json") 

    data = fo.create_json_output(copy_grid, input_files, goal_files, start_positions, gas, initial_time)
    fo.save_to_json(data, output_file)

