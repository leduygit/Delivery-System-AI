import heapq

class Graph:
    def __init__(self):
        self.edges = {}
        self.map = {}
    
    def add_edge(self, from_node, to_node, weight=1):
        if from_node not in self.edges:
            self.edges[from_node] = []

        self.edges[from_node].append((to_node, weight))
    
    def get_neighbors(self, node):
        return self.edges.get(node, [])
    
    def get_nodes_values(self, node):
        return self.map.get(node, None)

    
    def load_from_file(self, filename):
        raise NotImplementedError("Subclasses should implement the load_from_file method")

class GridGraph(Graph):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.create_edges()
        self.create_map()
    
    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def create_edges(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for x in range(self.rows):
            for y in range(self.cols):

                if self.grid[x][y] == 1:
                    continue

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy

                    if self.is_valid(nx, ny):
                        self.add_edge((x, y), (nx, ny), 1)

    def create_map(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.map[(x, y)] = self.grid[x][y]

