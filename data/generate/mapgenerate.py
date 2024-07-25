import numpy as np
import random
from collections import deque


class MapGenerator:
    def __init__(self, row, col, clusterSize=3, numClusters=None, favorCorners=False):
        self.row = row
        self.col = col
        self.clusterSize = clusterSize
        self.numClusters = (
            numClusters
            if numClusters is not None
            else (row * col) // (clusterSize * clusterSize)
        )
        self.favorCorners = favorCorners
        self.mapGrid = np.zeros((row, col), dtype=object)

    def generateMap(self):
        while True:
            for _ in range(self.numClusters):
                self._addCluster()
            if self.isConnected():
                break
            self.mapGrid = np.zeros((self.row, self.col), dtype=object)
        return self.mapGrid

    def _addCluster(self):
        clusterLength = random.randint(2, self.clusterSize)
        clusterDirection = random.choice([(0, 1), (1, 0)])  # Horizontal or Vertical
        startX, startY = (
            random.randint(0, self.row - 1),
            random.randint(0, self.col - 1),
        )

        for i in range(clusterLength):
            x, y = (
                startX + i * clusterDirection[0],
                startY + i * clusterDirection[1],
            )
            if 0 <= x < self.row and 0 <= y < self.col:
                self.mapGrid[x, y] = -1

    def _isValid(self, x, y):
        return 0 <= x < self.row and 0 <= y < self.col and self.mapGrid[x, y] == 0

    def _neighbors(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self._isValid(x + dx, y + dy):
                yield x + dx, y + dy

    def _checkOpponent(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.row and 0 <= y + j < self.col:
                    if str(self.mapGrid[x + i, y + j]).startswith("S"):
                        return True
        return False

    def _favorCornerPositions(self):
        corners = []
        for i in range(0, self.row, self.row - 1):
            for j in range(0, self.col, self.col - 1):
                count = sum(
                    1
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= i + dx < self.row
                    and 0 <= j + dy < self.col
                    and str(self.mapGrid[i + dx, j + dy]) != "-1"
                )
                if count <= 2:
                    corners.append((i, j))
        return random.choice(corners)

    def _randomPosition(self, isStart=False):
        if isStart and self.favorCorners and random.random() < 0.3:
            return self._favorCornerPositions()
        return random.randint(0, self.row - 1), random.randint(0, self.col - 1)

    def addStartGoal(self, S="S", G="G"):
        while True:
            start, goal = self._randomPosition(isStart=True), self._randomPosition()
            if (
                self.mapGrid[start[0], start[1]] == 0
                and self.mapGrid[goal[0], goal[1]] == 0
                and not self._checkOpponent(*start)
            ):
                path = self._bfs(start, goal)
                if path and len(path) > 1.1 * max(self.row, self.col):
                    self.mapGrid[start[0], start[1]] = S
                    self.mapGrid[goal[0], goal[1]] = G
                    return path

    def setFavorCorners(self, favorCorners):
        self.favorCorners = favorCorners

    def _bfs(self, start, goal):
        queue = deque([start])
        cameFrom = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = cameFrom[current]
                path.reverse()
                return path

            for neighbor in self._neighbors(*current):
                if neighbor not in cameFrom:
                    queue.append(neighbor)
                    cameFrom[neighbor] = current
        return []

    def _markReachable(self, x, y, visited):
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) not in visited:
                visited.add((cx, cy))
                for nx, ny in self._neighbors(cx, cy):
                    if (nx, ny) not in visited:
                        queue.append((nx, ny))

    def isConnected(self):
        visited = set()
        for x in range(self.row):
            for y in range(self.col):
                if self.mapGrid[x, y] == 0:
                    self._markReachable(x, y, visited)
                    break
            if visited:
                break

        return all(
            self.mapGrid[x, y] != 0 or (x, y) in visited
            for x in range(self.row)
            for y in range(self.col)
        )

    def addPlayers(self, numberPlayers=1):
        for i in range(numberPlayers):
            suffix = "" if i == 0 else str(i)
            self.addStartGoal(S=f"S{suffix}", G=f"G{suffix}")


if __name__ == "__main__":
    # lv = [(5,5), (10,10), (15,15), (20,20), (25,25), (28, 40)]
    lv = {
        "map1": (5, 5),
        "map2": (10, 10),
        "map3": (15, 15),
        "map4": (20, 20),
        "map5": (25, 25),
        "map6": (28, 40),
    }
    for item in ["lv1", "lv2", "lv3", "lv4"]:
        for name, level in lv.items():
            clusterSize = int(level[0] // 4 + 1)  # size of each obstacle cluster
            numClusters = int((level[0] + level[1]) * 0.8)  # number of clusters
            mapGen = MapGenerator(level[0], level[1], clusterSize, numClusters)
            mapGrid = mapGen.generateMap()
            mapGen.addPlayers(1)

            # Output with format
            for row in mapGrid:
                for cell in row:
                    print(str(cell).rjust(2), end=" ")
                print()

            # Output to file
            with open(f"Asset/Maps/{item}/{name}.txt", "w") as f:
                f.write(f"{level[0]} {level[1]} 100 100\n")
                for row in mapGrid:
                    for cell in row:
                        f.write(f"{cell} ")
                    f.write("\n")
