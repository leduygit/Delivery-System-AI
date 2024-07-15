import graph, solution as solution

def load_data(path):
    with open(path, 'r') as f:
        # Read grid dimensions
        rows, cols = map(int, f.readline().split())
        
        # Read grid data
        grid = []
        for _ in range(rows):
            grid.append(list(map(int, f.readline().split())))
        
        # Read gas limit
        gas = int(f.readline().strip())
        
        # Read agents
        agent_list = []
        agents = {}
        
        while True:
            line = f.readline().strip()
            if not line: 
                break
            
            agent_id = line
            start_pos = tuple(map(int, f.readline().split()))
            goal_pos = tuple(map(int, f.readline().split()))
            
            agent_list.append((start_pos, goal_pos))
            agents[agent_id] = (start_pos, goal_pos)
            
        return grid, agent_list, gas


def main():
    grid, agent_list, gas = load_data('input.txt')
    g = graph.GridGraph(grid)
    s = solution.TestSolution(g, agent_list, grid)
    result = s.solve()
    print(result)
    s.save_move_logs('output.json')

if __name__ == '__main__':
    main()