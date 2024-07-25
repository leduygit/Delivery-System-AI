import os
from random import randint
from search_logic.bots.random_bot import RandomBot
from search_logic.main import load_data
import search_logic.format_output as fo


def is_valid_move(grid, ox, oy, nx, ny):
    return 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and \
           grid[nx][ny] != -1 and abs(nx - ox) + abs(ny - oy) == 1


def apply_moves(grid, start_position, move, index):
    grid[start_position[0]][start_position[1]] = '.'
    grid[move[0]][move[1]] = 'S{}'.format(index)
    return grid


def print_current(positions, goals):
    for i, pos in enumerate(positions):
        with open('search_logic/agents/agent_{}.txt'.format(i + 1), 'a') as f:
            f.write('{} {}\n'.format(pos[0], pos[1]))

    for i, goal in enumerate(goals):
        with open('search_logic/agents/goal_{}.txt'.format(i + 1), 'a') as f:
            f.write('{} {}\n'.format(goal[0], goal[1]))


def get_new_goal(grid, current_position):
    places = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.':
                places.append((i, j))
    
    if not places:
        return current_position
    index = randint(0, len(places) - 1)
    return places[index]


def runner():
    grid, start_positions, time, gas = load_data('search_logic/input4.txt')

    print(start_positions)
    copy_grid = [list(row) for row in grid]
    os.makedirs('agents', exist_ok=True)
    mmap = {
        'grid': grid,
        'height': len(grid),
        'width': len(grid[0]),
    }
    # [[(1, 1), (7, 8)], [(2, 5), (9, 0)], [(8, 5), (4, 6)]]
    current_positions = [pos[0] for pos in start_positions]
    current_goals = [pos[1] for pos in start_positions]
    print(current_positions)
    print(current_goals)
    bots = [RandomBot() for _ in current_positions]

    for i, bot in enumerate(bots):
        with open('search_logic/agents/agent_{}.txt'.format(i + 1), 'w') as f:
            f.write("")
        with open('search_logic/agents/goal_{}.txt'.format(i + 1), 'w') as f:
            f.write("")

    while time:
        for i, bot in enumerate(bots):
            state = {
                'x': current_positions[i][0],
                'y': current_positions[i][1],
            }
            move = bot.get_move(mmap, state)
            print(move)
            if move is None or not is_valid_move(mmap['grid'], 
                                                    current_positions[i][0], current_positions[i][1],
                                                    move[0], move[1]):
                print_current(current_positions, current_goals)
                continue
            mmap['grid'] = apply_moves(mmap['grid'], current_positions[i], move, i)
            if move == current_goals[i]:
                current_goals[i] = get_new_goal(mmap['grid'], current_positions[i])
            current_positions[i] = move
            print_current(current_positions, current_goals)
        time -= 1

    input_files = [f'search_logic/agents/agent_{i+1}.txt' for i in range(len(bots))]
    output_file = 'Assets/Json/lv4/output.json'
    
    # Create JSON output data
    data = fo.create_json_output(copy_grid, input_files, start_positions)
    
    # Save JSON to file
    fo.save_to_json(data, output_file)