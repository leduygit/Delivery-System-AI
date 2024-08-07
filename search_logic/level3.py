from search_logic.solution import SolutionBase
from queue import PriorityQueue

def get_value(value):
    if isinstance(value, tuple):
        return value[1]
    try:
        return int(value)
    except:
        return 0


class Level3(SolutionBase):
    def __init__(self, graph, agent_list, map_data, time=None, gas=None):
        super().__init__(graph, agent_list, map_data, time=time, gas=gas)

    def get_level(self):
        return "lv3"

    def solve(self):
        start, goal = self.agent_list[0]
        orginal_map = self.map_data.copy()
        marked = set()
        pq = PriorityQueue()
        pq.put((0, self.gas, self.time, start, [start]))
        marked.add((start, self.gas, self.time))

        while not pq.empty():
            cost, gas, time, current, path = pq.get()

            if time < 0:
                continue
            if current == goal:
                # print('COST:', cost)
                # print('TIME:', time)
                # print('GAS:', gas)
                self.move_logs = self.trace_path(orginal_map, path)
                return "\n".join([f"{x} {y}" for x, y in path[1:]])

            if len(path) > self.graph.rows * self.graph.cols:
                continue
            for neighbor, ctime in self.graph.get_neighbors(current):
                newGas = gas - 1
                if ctime > 1:
                    pass
                    # print(neighbor, ctime)
                # Check if neighbor is gas station
                if ctime < 0:
                    ctime = abs(ctime) + 1
                    newGas = self.gas

                if newGas < 0:
                    continue
                if (time < 0):
                    continue
                if (neighbor, newGas, time - ctime) in marked:
                    continue

                marked.add((neighbor, newGas, time - ctime))
                pq.put((cost + 1, newGas, time - ctime, neighbor, path + [neighbor]))

        return "FAIL"
