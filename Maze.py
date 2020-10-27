from Node import Node
from random import randrange
from random import seed
from pygame import Color
from pygame import display

class Maze:

    WALL_COLOR = Color(100, 100, 100) #150 0 200
    PATH_COLOR = Color(255, 255, 255)
    ENTRANCE_COLOR = Color(255, 0, 0)

    def __init__(self, width, height, surface):
        self.rows = height
        self.cols = width
        self.grid = []
        self.surface = surface
        seed(0)
        self.initialize()
        self.createEntranceAndExit()

    def initialize(self):
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                node = Node(j, i, Maze.WALL_COLOR)
                self.grid[i].append(node)

    def createEntranceAndExit(self):
        entrance = randrange(0, self.rows // 2) * 2
        entrance += 1
        self.entrance = self.grid[entrance][0]
        self.entrance.isWall = False

        exit = randrange(0, self.rows // 2) * 2
        exit += 1
        self.exit = self.grid[exit][self.cols - 1]
        self.exit.isWall = False

        self.entrance.changeColor(Maze.ENTRANCE_COLOR)
        self.exit.changeColor(Maze.ENTRANCE_COLOR)

    def render(self):
        for row in self.grid:
            for node in row:
                node.draw(self.surface)
        display.update()

    def __str__(self):
        string = ""
        for row in self.grid:
            for node in row:
                string += str(node)
            string += "\n"
        return string
