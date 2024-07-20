import graph
import solution
import SampleSolution as sample
import format_output as fo

def load_data(path):
    with open(path, 'r') as f:
        # Read the first line for n, m, time, and gas
        n, m, time, gas = map(int, f.readline().split())
        
        # Read the grid
        grid = []
        for _ in range(n):
            grid.append(f.readline().strip().split())
        
        # Initialize an array to store start ('S') and goal ('G') positions
        start_goal_positions = [[] for _ in range(10)]
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'S':
                    start_goal_positions[0].append((i, j))
                elif grid[i][j] == 'G':
                    start_goal_positions[0].append((i, j))
                elif grid[i][j].startswith('S'):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                elif grid[i][j].startswith('G'):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                else:
                    grid[i][j] = int(grid[i][j])
        
        # Validate and store agent positions
        if not start_goal_positions[0] or len(start_goal_positions[0]) < 2:
            raise ValueError("Error: Expected at least one 'S' and one 'G' in the grid.")
        
        # Remove empty positions from agent list
        start_goal_positions = [positions for positions in start_goal_positions if positions]
        
    return grid, start_goal_positions, time, gas

def main():
    grid, agent_list, time, gas = load_data('input.txt')
    print(type(time), type(gas))

    g = graph.GridGraph(grid)

    s = sample.TestSolution(g, agent_list, grid, time, gas)
    s.solve()

    s.save_move_logs('moves.txt')

    input_files = [f'agents/agent_{i+1}.txt' for i in range(len(agent_list))]  # Assuming file names are in agents/agent_1.txt, agents/agent_2.txt, etc.
    #input_files = ['moves.txt']
    output_file = 'output.json'
    
    # Create JSON output data
    data = fo.create_json_output(grid, input_files)
    
    # Save JSON to file
    fo.save_to_json(data, output_file)

if __name__ == "__main__":
    main()
