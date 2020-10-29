from Node import Node
from random import randrange
from random import seed
from pygame import Color
from pygame import display

class Maze:
    """Used to represent a maze board.
    -WALL_COLOR: pygame Color object. Color used for all walls.
    -PATH_COLOR: pygame Color object. Color used for all paths.
    -ENTRANCE_COLOR: pygame Color object. Color used for the entrance and exit."""

    WALL_COLOR = Color(100, 100, 100)               #Dark Gray
    PATH_COLOR = Color(255, 255, 255)               #White
    ENTRANCE_COLOR = Color(255, 0, 0)               #Red

    def __init__(self, width, height, surface):
        """
        -height: int. number of rows the maze will have. Stored in self.rows
        -width: int. number of columns the maze will have. Stored in self.cols
        -surface: pygame surface. Used for rendering. Stored in self.surface
        -self.grid: a double array used to store all nodes."""

        self.rows = height + (1 - (height % 2))
        self.cols = width + (1 - (width % 2))
        self.grid = []
        self.surface = surface

        seed()

        self.initialize()
        self.createEntranceAndExit()

    def initialize(self):
        """Creates a double array of nodes. All nodes are walls upon creation."""

        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                node = Node(j, i, Maze.WALL_COLOR)
                self.grid[i].append(node)

    def createEntranceAndExit(self):
        """Creates an entrance and an exit. Entrance is on the left side of the
        maze. Exit is on the right side of the maze.
        Both entrance and exit are saved as class attributes for future algorithm
        reference."""

        entrance = randrange(0, self.rows // 2) * 2
        entrance += 1
        self.entrance = self.grid[entrance][0]
        self.entrance.isWall = False

        exit = randrange(0, self.rows // 2) * 2
        exit += 1
        self.exit = self.grid[exit][self.cols - 1]
        self.exit.isWall = False

        self.entrance.color = Maze.ENTRANCE_COLOR
        self.exit.color = Maze.ENTRANCE_COLOR


    def reset(self):
        """Turns all paths back to walls and generates a new entrance and exit."""

        for row in self.grid:
            for node in row:
                node.isWall = True
                node.visited = False
        self.createEntranceAndExit()
        self.clear()

    def clear(self):
        """Clears the maze after traversal. Changes colors back to normal."""

        for row in self.grid:
            for node in row:
                if node.isWall:
                    node.color = self.WALL_COLOR
                else:
                    if node == self.entrance or node == self.exit:
                        node.color = self.ENTRANCE_COLOR
                    else:
                        node.color = self.PATH_COLOR

        self.render()

    def render(self):
        """Draws all nodes and renders at the end."""

        for row in self.grid:
            for node in row:
                node.draw(self.surface)
        display.update()

    def __str__(self):
        """String representation of maze. Walls are represented by #'s. Paths are
        represented by .'s (dots).
        Mainly used for debugging."""

        string = ""
        for row in self.grid:
            for node in row:
                string += str(node)
            string += "\n"
        return string
