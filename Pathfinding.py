from Maze import Maze
from pygame import Color
from pygame import time
from Node import Node

"""*****************************HUGH RIGHT-WALL-METHOD****************************"""
class HugRightWall:

    PATH_COLOR = Color(0, 0, 200)
    VISITED_COLOR = Color(0, 200, 150)
    CURRENT_COLOR = Color(255, 140, 0)

    WAIT_TIME = 20

    def __init__(self, maze, animate):
        self.maze = maze
        self.animate = animate

        self.x = maze.entrance.x
        self.y = maze.entrance.y
        self.visited = []

        self.traverse()

        if not animate:
            maze.render()

    def traverse(self):

        move = self.moveRight

        while self.x != self.maze.cols - 1:

            self.changeNodeColor(self.maze.grid[self.y][self.x], self.CURRENT_COLOR)

            move = self.nextMove(move)
            move()

        self.createPath()

    def move(self):
        current = (self.x, self.y)
        if current in self.visited:
            self.visited.pop()
        else:
            self.visited.append(current)

        self.changeNodeColor(self.maze.grid[self.y][self.x], self.VISITED_COLOR, 0)

    def canMoveRight(self):

        if self.maze.grid[self.y][self.x + 1].isWall:
            return False
        return True

    def moveRight(self):

        self.move()
        self.x += 1

    def canMoveDown(self):

        if self.maze.grid[self.y + 1][self.x].isWall:
            return False
        return True

    def moveDown(self):

        self.move()
        self.y += 1

    def canMoveLeft(self):

        if self.maze.grid[self.y][self.x - 1].isWall:
            return False
        return True

    def moveLeft(self):

        self.move()
        self.x -= 1

    def canMoveUp(self):

        if self.maze.grid[self.y - 1][self.x].isWall:
            return False
        return True

    def moveUp(self):

        self.move()
        self.y -= 1

    def nextMove(self, move):

        if move == self.moveDown:
            if self.canMoveLeft():
                return self.moveLeft
            elif self.canMoveDown():
                return move
            elif self.canMoveRight():
                return self.moveRight
            return self.moveUp
        elif move == self.moveLeft:
            if self.canMoveUp():
                return self.moveUp
            elif self.canMoveLeft():
                return move
            elif self.canMoveDown():
                return self.moveDown
            return self.moveRight
        elif move == self.moveUp:
            if self.canMoveRight():
                return self.moveRight
            elif self.canMoveUp():
                return move
            elif self.canMoveLeft():
                return self.moveLeft
            return self.moveDown
        else:
            if self.canMoveDown():
                return self.moveDown
            elif self.canMoveRight():
                return move
            elif self.canMoveUp():
                return self.moveUp
            return self.moveLeft

    def createPath(self):

        for coord in self.visited:
            self.changeNodeColor(self.maze.grid[coord[1]][coord[0]], self.PATH_COLOR, .5)
        self.changeNodeColor(self.maze.exit, self.PATH_COLOR, 0)

    def changeNodeColor(self, node, color, multiplier=1):

        node.changeColor(color)
        if self.animate:
            node.render(self.maze.surface)
            if multiplier != 0:
                time.wait( int(self.WAIT_TIME * multiplier))
        else:
            node.draw(self.maze.surface)

"""*****************************END OF HUGH-RIGHT-WALL****************************"""


"""*******************************A* SEARCH METHOD********************************"""
class A_Star:

    PATH_COLOR = Color(0, 0, 200)
    TO_VISIT_COLOR = Color(255, 140, 0)
    VISITED_COLOR = Color(0, 200, 150)

    WAIT_TIME = 20

    class A_Node(Node):

        exit = None

        #g -> distance from the start, h -> distance from the end, f -> g + h
        def __init__(self, current, parent):

            if parent is None:
                self.g = 0
            else:
                self.g = parent.g + 1
            self.h = abs(self.exit.x - current.x) + abs(self.exit.y - current.y)
            self.parent = parent
            Node.__init__(self, current.x, current.y, current.color)
            self.isWall = current.isWall

        @property
        def f(self):
            return self.g + self.h

        def update(self, parent):
            self.g = parent.g + 1
            self.parent = parent


    def __init__(self, maze, animate):
        self.visited = []
        self.toVisit = []
        self.maze = maze
        self.animate = animate

        self.A_Node.exit = maze.grid[maze.exit.y][maze.exit.x]
        for row in range(maze.rows):
            for col in range(maze.cols):
                maze.grid[row][col] = self.A_Node(maze.grid[row][col], None)
        self.A_Node.exit = maze.grid[maze.exit.y][maze.exit.x]

        node = maze.grid[maze.entrance.y][maze.entrance.x]
        self.toVisit.append(node)
        self.generate()

        if not animate:
            maze.render()

    def generate(self):

        while True:
            #print(self.toVisit)
            current = min(self.toVisit, key=self.getF)
            self.toVisit.remove(current)
            self.visited.append(current)
            self.changeNodeColor(current, self.VISITED_COLOR)

            if current is self.A_Node.exit:
                break

            for neighbor in self.getNeighbors(current):

                #print(neighbor.x, neighbor.y)

                if neighbor in self.visited:
                    continue

                if neighbor.parent is None or neighbor.f > current.f + 1:

                    neighbor.update(current)

                    if neighbor not in self.toVisit:
                        #print(neighbor.x, neighbor.y)
                        self.toVisit.append(neighbor)
                        self.changeNodeColor(neighbor, self.TO_VISIT_COLOR)

        self.displayPath()

    def getF(self, node):
        return node.f

    def getNeighbors(self, node):

        neighbors = []

        if self.canMoveRight(node):
            neighbors.append(self.maze.grid[node.y][node.x + 1])
        if self.canMoveDown(node):
            neighbors.append(self.maze.grid[node.y + 1][node.x])
        if self.canMoveLeft(node):
            neighbors.append(self.maze.grid[node.y][node.x - 1])
        if self.canMoveUp(node):
            neighbors.append(self.maze.grid[node.y - 1][node.x])

        return neighbors

    def canMoveRight(self, node):
        if node.x == self.maze.cols - 1 or self.maze.grid[node.y][node.x + 1].isWall:
            return False
        return True

    def canMoveDown(self, node):
        if self.maze.grid[node.y + 1][node.x].isWall:
            return False
        return True

    def canMoveLeft(self, node):
        if node.x == 0 or self.maze.grid[node.y][node.x - 1].isWall:
            return False
        return True

    def canMoveUp(self, node):
        if self.maze.grid[node.y - 1][node.x].isWall:
            return False
        return True

    def displayPath(self):

        current = self.A_Node.exit
        while current is not None:
            self.changeNodeColor(current, self.PATH_COLOR, .5)
            current = current.parent

    def changeNodeColor(self, node, color, multiplier=1):

        node.changeColor(color)
        if self.animate:
            node.render(self.maze.surface)
            if multiplier != 0:
                time.wait(int(self.WAIT_TIME * multiplier))
        else:
            node.draw(self.maze.surface)

"""***************************END A* PATHFINDING******************************"""
