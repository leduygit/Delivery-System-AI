import os
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


def print_current(positions):
    for i, pos in enumerate(positions):
        with open('agents/agent_{}.txt'.format(i + 1), 'a') as f:
            f.write('{} {}\n'.format(pos[0], pos[1]))


def runner():
    grid, start_positions, time, gas = load_data('search_logic/input4.txt')
    os.makedirs('agents', exist_ok=True)
    mmap = {
        'grid': grid,
        'height': len(grid),
        'width': len(grid[0]),
    }
    current_positions = [pos[0] for pos in start_positions]
    current_goals = [pos[1] for pos in start_positions]
    bots = [RandomBot() for _ in current_positions]

    for i, bot in enumerate(bots):
        with open('agents/agent_{}.txt'.format(i + 1), 'w') as f:
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
                print_current(current_positions)
                continue
            mmap['grid'] = apply_moves(mmap['grid'], current_positions[i], move, i)
            current_positions[i] = move
            print_current(current_positions)
        time -= 1

    input_files = [f'agents/agent_{i+1}.txt' for i in range(len(bots))]
    output_file = 'Assets/Json/lv4/output.json'
    
    # Create JSON output data
    data = fo.create_json_output(grid, input_files)
    
    # Save JSON to file
    fo.save_to_json(data, output_file)