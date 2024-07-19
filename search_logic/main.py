import graph, solution as solution, level1, level2

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
        
    return grid, start_goal_positions, time, gas



def main():
    grid, agent_list, time, gas = load_data('input2.txt')

    print(grid)

    g = graph.GridGraph(grid)
    l1 = level1.BasicLevel(g, agent_list, grid)
    
    l1_BFS = l1.BFS()
    print("BFS")
    l1.save_move_logs('l1_BFS.json')
    l1_DFS = l1.DFS()
    print("DFS")
    l1.save_move_logs('l1_DFS.json')
    l1_GBFS = l1.GBFS()
    print("GBFS")
    l1.save_move_logs('l1_GBFS.json')
    l1_UCS = l1.UCS()
    print("UCS")
    l1.save_move_logs('l1_UCS.json')
    l1_Astar = l1.Astar()
    print("A*")
    l1.save_move_logs('l1_Astar.json')
    
    l2 = level2.TimeLimitLevel(g, agent_list, grid, time)
    l2.solve()
    print("Time Limit Level")
    l2.save_move_logs('l2.json')
    
    

if __name__ == '__main__':
    main()