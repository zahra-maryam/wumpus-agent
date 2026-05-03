import random

class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]
        self.place_hazards()

    def place_hazards(self):
        # Place Wumpus
        wx, wy = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
        self.grid[wx][wy] = "W"

        # Place pits
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


class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def tell(self, clause):
        self.clauses.append(clause)

    def resolve(self, query):
        # Simplified resolution simulation
        steps = 0
        for clause in self.clauses:
            steps += 1
            if query in clause:
                return False, steps  # contradiction not found
        return True, steps  # assume safe if no contradiction


class Agent:
    def __init__(self, world):
        self.world = world
        self.kb = KnowledgeBase()
        self.position = (0, 0)
        self.visited = set()
        self.inference_steps = 0

    def perceive_and_update(self):
        x, y = self.position
        percepts = self.world.get_percepts(x, y)

        for p in percepts:
            self.kb.tell(f"{p}_{x}_{y}")

        return percepts

    def is_safe(self, x, y):
        safe, steps = self.kb.resolve(f"Safe_{x}_{y}")
        self.inference_steps += steps
        return safe

    def move(self):
        x, y = self.position
        directions = [(1,0), (0,1), (-1,0), (0,-1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.world.rows and 0 <= ny < self.world.cols:
                if (nx, ny) not in self.visited and self.is_safe(nx, ny):
                    self.position = (nx, ny)
                    self.visited.add((nx, ny))
                    return self.position

        return self.position