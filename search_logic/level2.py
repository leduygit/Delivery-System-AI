from search_logic.solution import SolutionBase
from queue import PriorityQueue as p_queue
    
class Level2(SolutionBase):
    def __init__(self, graph, agent_list, map_data, time=None):
        super().__init__(graph, agent_list, map_data, time=time)

    def get_level(self):
        return 'lv2'

    def trace_path(self, path):
        move_logs = []
        for i in range(len(path)):
            move_logs.append((path[i]))
        return move_logs
      
    def get_heuristic(self, node, goal):
        r = node[0]
        c = node[1]
        if self.map_data[r][c] == -1:
            return 1000000
        if isinstance(self.map_data[r][c], int):
            return abs(r - goal[0]) + abs(c - goal[1]) + self.map_data[r][c] + 1
        return abs(r - goal[0]) + abs(c - goal[1])

    def solve(self):
        start, goal = self.agent_list[0]
        marked = set()
        pq = p_queue()
        pq.put((0, self.time, start, [start]))
        marked.add((start, self.time))

        while not pq.empty():
            cost, time, current, path = pq.get()
            
            if time < 0:
                continue

            # print(current, time, gas)
            if current == goal:
                print('COST:', cost)
                print('TIME:', time)
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])
        
            if len(path) > self.graph.rows * self.graph.cols:
                continue
        
            for neighbor, ctime in self.graph.get_neighbors(current):
                if (self.map_data[neighbor[0]][neighbor[1]] != 0):
                        ctime += 1
                if (neighbor, time - ctime) in marked:
                    continue
                marked.add((neighbor, time - ctime))
                pq.put((cost + 1, time - ctime, neighbor,
                        path + [neighbor]))

        return 'FAIL'