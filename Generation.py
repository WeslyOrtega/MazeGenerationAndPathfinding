from random import randrange
from pygame import time

class DepthFirst:
    """Algorithm that generates mazes by creating paths until there isn't a direction
    to move, and then backtracks until it can find another path to create. If it
    does not find a path to generate, then the whole maze has been generated.
    -WAIT_TIME: int. The time (in ms) in between generation steps. Used to animate
    maze generation."""

    WAIT_TIME = 5                       #Wait time between steps during animation

    def __init__(self, maze, animate):
        """
        -maze: A Maze object. Stored in self.maze
        animate: Boolean. Determines whether generation steps will be shown.
            Stored in self.animate."""

        self.maze = maze
        self.animate = animate
        maze.render()
        self.generate(1, maze.entrance.y)   #Start generation next to the entrance
        if not animate:
            maze.render()

    def generate(self, x, y):
        """Recursively regenerates maze. Current point is turned to a path, and
        then attempts to make a path in all directions (up, down, left, right),
        order chosen at random. Once it cannot move, it backtracks to the last
        point where a path can be made."""

        current = self.maze.grid[y][x]
        self.clearNode(current)

        previous = []           #Keeps track of all the directions that have been attempted

        while len(previous) < 4:    #Checks that a path in all directions has been attempted
            direction = randrange(0, 4) #0 right, 1 left, 2 up, 3 down

            if direction in previous:
                continue

            if direction == 0 and self.canMoveRight(x, y):
                neighbor = self.maze.grid[y][x + 1]
                self.clearNode(neighbor)
                self.generate(x + 2, y)
            elif direction == 1 and self.canMoveLeft(x, y):
                neighbor = self.maze.grid[y][x - 1]
                self.clearNode(neighbor)
                self.generate(x - 2, y)
            elif direction == 2 and self.canMoveUp(x, y):
                neighbor = self.maze.grid[y - 1][x]
                self.clearNode(neighbor)
                self.generate(x, y - 2)
            elif direction == 3 and self.canMoveDown(x, y):
                neighbor = self.maze.grid[y + 1][x]
                self.clearNode(neighbor)
                self.generate(x, y + 2)

            previous.append(direction)

    def clearNode(self, node):
        """Converts [node] into a path"""

        node.visited = True
        node.isWall = False

        self.changeNodeColor(node)

    def canMoveRight(self, x, y):
        """Checks if a path can be made to the right.
        Checks that the current node is not next to the right edge, and that there
        isn't already an existing path to the right."""

        if (x + 1) != (self.maze.cols - 1) and not self.maze.grid[y][x + 2].visited:
            return True
        return False

    def canMoveLeft(self, x, y):
        """Checks if a path can be made to the left.
        Checks that the current node is not next to the left edge, and that there
        isn't already an existing path to the left."""

        if not (x - 1) <= 0 and not self.maze.grid[y][x - 2].visited:
            return True
        return False

    def canMoveUp(self, x, y):
        """Checks if a path can be made upwards.
        Checks that the current node is not next to the top edge, and that there
        isn't already an existing path upwards."""

        if (y - 1) != 0 and not self.maze.grid[y - 2][x].visited:
            return True
        return False

    def canMoveDown(self, x, y):
        """Checks if a path can be made downwards.
        Checks that the current node is not next to the bottom edge, and that there
        isn't already an existing path downwards."""

        if (y + 1) != (self.maze.rows - 1) and not self.maze.grid[y + 2][x].visited:
            return True
        return False

    def changeNodeColor(self, node):
        """Changes [node]'s color. If animation is turned on (self.animation = True),
        immediately render. Otherwise, just draw it; rendering will happen once
        the entire maze has been rendered."""

        node.color = self.maze.PATH_COLOR
        if self.animate:
            node.render(self.maze.surface)
            time.wait(self.WAIT_TIME)
        else:
            node.draw(self.maze.surface)
