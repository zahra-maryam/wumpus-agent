import random

class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]
        self.place_hazards()

    def place_hazards(self):
        wx, wy = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
        self.grid[wx][wy] = "W"

        for _ in range((self.rows * self.cols)//5):
            x, y = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if self.grid[x][y] == "":
                self.grid[x][y] = "P"

    def get_percepts(self, x, y):
        percepts = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.grid[nx][ny] == "P":
                    percepts.append("Breeze")
                if self.grid[nx][ny] == "W":
                    percepts.append("Stench")

        return list(set(percepts))


class Agent:
    def __init__(self, world):
        self.world = world
        self.position = (0, 0)
        self.visited = set()
        self.inference_steps = 0
        self.safe = set()
        self.danger = set()

    def perceive_and_update(self):
        percepts = self.world.get_percepts(*self.position)
        x, y = self.position

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.world.rows and 0 <= ny < self.world.cols:
                if "Breeze" in percepts or "Stench" in percepts:
                    self.danger.add((nx, ny))
                else:
                    self.safe.add((nx, ny))

        return percepts
        
def move(self):
    x, y = self.position
    directions = [(1,0), (0,1), (-1,0), (0,-1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) in self.safe and (nx, ny) not in self.visited:
            self.position = (nx, ny)
            self.visited.add((nx, ny))
            self.inference_steps += 1
            return self.position

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in self.visited:
            self.position = (nx, ny)
            self.visited.add((nx, ny))
            self.inference_steps += 1
            return self.position

    return self.position