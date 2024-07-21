from solution import SolutionBase
from queue import PriorityQueue


class Level3(SolutionBase):
    def __init__(self, graph, agent_list, map_data, time=None, gas=None):
        super().__init__(graph, agent_list, map_data, time=time, gas=gas)

    def trace_path(self, path):
        move_logs = []
        for i in range(len(path)):
            move_logs.append((path[i]))
        return move_logs

    def solve(self):
        start, goal = self.agent_list[0]
        costs = {(r, c): 100000 for r in range(self.graph.rows)
                 for c in range(self.graph.cols)}
        times = {(r, c): 0 for r in range(self.graph.rows)
                 for c in range(self.graph.cols)}
        gases = {(r, c): 0 for r in range(self.graph.rows)
                 for c in range(self.graph.cols)}
        pq = PriorityQueue()
        pq.put((0, self.gas, self.time, start, [start]))
        costs[start] = 0
        times[start] = self.time
        gases[start] = self.gas

        while not pq.empty():
            cost, gas, time, current, path = pq.get()

            if current == goal:
                print('COST:', cost)
                print('TIME:', time)
                print('GAS:', gas)
                self.move_logs = self.trace_path(path)
                return '\n'.join([f'{x} {y}' for x, y in path[1:]])

            if len(path) > self.graph.rows * self.graph.cols:
                continue
            if time < 1:
                continue
            for neighbor, weight in self.graph.get_neighbors(current):
                newGas = gas - 1
                # Check if neighbor is gas station
                if weight < 0:
                    weight = abs(weight)
                    newGas = self.gas

                if newGas < 0:
                    continue

                if costs[neighbor] <= cost + weight and \
                   gases[neighbor] > gas - 1:
                    continue

                costs[neighbor] = cost + weight
                times[neighbor] = time - 1
                gases[neighbor] = newGas
                pq.put((costs[neighbor], newGas, time - 1, neighbor,
                        path + [neighbor]))

        return 'FAIL'
