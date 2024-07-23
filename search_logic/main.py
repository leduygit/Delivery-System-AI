import search_logic.graph as graph
import search_logic.SampleSolution as sample
import search_logic.level1 as lv1
import search_logic.level2 as lv2
import search_logic.format_output as fo
import search_logic.level1 as level1
import search_logic.level2 as level2

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
                    if (len(start_goal_positions[0]) > 1):
                        # reverse the order of the start and goal positions
                        start_goal_positions[0][0], start_goal_positions[0][1] = start_goal_positions[0][1], start_goal_positions[0][0]
                elif grid[i][j] == 'G':
                    start_goal_positions[0].append((i, j))
                elif grid[i][j].startswith('S'):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                    if (len(start_goal_positions[identifier]) > 1):
                        # reverse the order of the start and goal positions
                        start_goal_positions[identifier][0], start_goal_positions[identifier][1] = start_goal_positions[identifier][1], start_goal_positions[identifier][0]
                elif grid[i][j].startswith('G'):
                    identifier = int(grid[i][j][1:])
                    start_goal_positions[identifier].append((i, j))
                elif grid[i][j].startswith('F'):
                    grid[i][j] = ('F', int(grid[i][j][1:]))
                else:
                    grid[i][j] = int(grid[i][j])
        
        # Validate and store agent positions
        if not start_goal_positions[0] or len(start_goal_positions[0]) < 2:
            raise ValueError("Error: Expected at least one 'S' and one 'G' in the grid.")
        
        # Remove empty positions from agent list
        start_goal_positions = [positions for positions in start_goal_positions if positions]
        
    return grid, start_goal_positions, time, gas

def search_logic():
    grid, agent_list, time, gas = load_data('search_logic/input.txt')

    print(type(time), type(gas))

    g = graph.GridGraph(grid)
    
    #s = sample.TestSolution(g, agent_list, grid, time, gas)
    #s = lv1.GBFS(g, agent_list, grid)
    s = lv2.Level2(g, agent_list, grid, time)   
    s.solve()

    s.save_move_logs('search_logic/moves.txt')

    # input_files = [f'agents/agent_{i+1}.txt' for i in range(len(agent_list))]  # Assuming file names are in agents/agent_1.txt, agents/agent_2.txt, etc.
    input_files = ['search_logic/moves.txt']
    output_file = 'Assets/Json/' + s.get_level() + '/output.json'
    
    # Create JSON output data
    data = fo.create_json_output(grid, input_files)
    
    # Save JSON to file
    fo.save_to_json(data, output_file)