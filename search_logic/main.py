import graph, solution as solution, level1 as level1

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
        
        # Validate and store agent positions
        if not start_goal_positions[0] or not start_goal_positions[0]:
            print("Error: Expected at least one 'S' and one 'G' in the grid.")
        
    return grid, start_goal_positions, time, gas



def main():
    grid, agent_list, time, gas = load_data('input.txt')

    g = graph.GridGraph(grid)
    l1 = level1.BasicLevel(g, agent_list, grid)
    
    l1_BFS = l1.BFS()
    print("BFS")
    print(l1_BFS)
    l1.save_move_logs('l1_BFS.json')
    print("--------------------")
    l1_DFS = l1.DFS()
    print("DFS")
    print(l1_DFS)
    l1.save_move_logs('l1_DFS.json')
    print("--------------------")
    l1_A = l1.Astar()
    print("A*")
    print(l1_A)
    l1.save_move_logs('l1_Astar.json')
    
    


if __name__ == '__main__':
    main()