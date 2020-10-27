from random import randrange
from random import seed
from pygame import time

class DepthFirst:

    WAIT_TIME = 5

    def __init__(self, maze, animate):
        self.maze = maze
        self.animate = animate
        maze.render()
        seed(2)
        self.generate(1, maze.entrance.y)
        if not animate:
            maze.render()

    def generate(self, x, y):

        current = self.maze.grid[y][x]
        current.visited = True
        current.isWall = False

        self.changeNodeColor(current)

        previous = []

        while len(previous) < 4:
            direction = randrange(0, 4) #0 right, 1 left, 2 up, 3 down

            if direction in previous:
                continue

            if direction == 0 and self.canMoveRight(x, y):
                self.moveRight(x, y)
                self.generate(x + 2, y)
            elif direction == 1 and self.canMoveLeft(x, y):
                self.moveLeft(x, y)
                self.generate(x - 2, y)
            elif direction == 2 and self.canMoveUp(x, y):
                self.moveUp(x, y)
                self.generate(x, y - 2)
            elif direction == 3 and self.canMoveDown(x, y):
                self.moveDown(x, y)
                self.generate(x, y + 2)

            previous.append(direction)

    def canMoveRight(self, x, y):
        if (x + 1) != (self.maze.cols - 1) and not self.maze.grid[y][x + 2].visited:
            return True
        return False

    def moveRight(self, x, y):
        neighbor = self.maze.grid[y][x + 1]
        neighbor.visited = True
        neighbor.isWall = False

        self.changeNodeColor(neighbor)

    def canMoveLeft(self, x, y):
        if not (x - 1) <= 0 and not self.maze.grid[y][x - 2].visited:
            return True
        return False

    def moveLeft(self, x, y):
        neighbor = self.maze.grid[y][x - 1]
        neighbor.visited = True
        neighbor.isWall = False

        self.changeNodeColor(neighbor)

    def canMoveUp(self, x, y):
        if (y - 1) != 0 and not self.maze.grid[y - 2][x].visited:
            return True
        return False

    def moveUp(self, x, y):
        neighbor = self.maze.grid[y - 1][x]
        neighbor.visited = True
        neighbor.isWall = False

        self.changeNodeColor(neighbor)

    def canMoveDown(self, x, y):
        if (y + 1) != (self.maze.rows - 1) and not self.maze.grid[y + 2][x].visited:
            return True
        return False

    def moveDown(self, x, y):
        neighbor = self.maze.grid[y + 1][x]
        neighbor.visited = True
        neighbor.isWall = False

        self.changeNodeColor(neighbor)

    def changeNodeColor(self, node):

        node.changeColor(self.maze.PATH_COLOR)
        if self.animate:
            node.render(self.maze.surface)
            time.wait(self.WAIT_TIME)
        else:
            node.draw(self.maze.surface)
