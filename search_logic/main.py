import graph, solution as solution, level1, level2
import SampleSolution
# n m time gas
# map

# 5 5 -1 -1
# S 0 0 0 S1
# 0 1 1 1 0
# 0 1 1 1 0
# 0 1 1 1 0
# G1 0 0 0 G


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
        if not start_goal_positions[0] or not start_goal_positions[0]:
            print("Error: Expected at least one 'S' and one 'G' in the grid.")

        # remove empty positins from agent list
        start_goal_positions = [positions for positions in start_goal_positions if positions]
        
    return grid, start_goal_positions, time, gas



def main():
    grid, agent_list, time, gas = load_data('input.txt')

    # print(grid)

    g = graph.GridGraph(grid)

    s = SampleSolution.TestSolution(g, agent_list, grid)
    s.solve()
    s.save_to_json('test_output.json')

    heapSolution = SampleSolution.HeapSolution(g, agent_list, grid)
    heapSolution.solve()
    heapSolution.save_to_json('heap_output.json')
    
if __name__ == '__main__':
    main()