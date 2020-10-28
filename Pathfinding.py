from Maze import Maze
from pygame import Color
from pygame import time
from Node import Node

"""*****************************HUGH RIGHT-WALL-METHOD****************************"""
class HugRightWall:
    """Algorithm that traverses a maze by prioritizing right turns. Move higherchy
    goes as right_turn > moving_forward > left_turn > moving_backwards.
    -PATH_COLOR: pygame Color object. Used for path from the entrance to the exit.
    -VISITED_COLOR: pygame Color object. Used for visited nodes that are not in
        direct path from the entrance to the exit.
    -CURRENT_COLOR: pygame Color object. Used to show the algorithm's current position.
    -WAIT_TIME: int. The time (in ms) in between generation steps. Used to animate
    maze traversal."""

    PATH_COLOR = Color(0, 0, 200)
    VISITED_COLOR = Color(0, 200, 150)
    CURRENT_COLOR = Color(255, 140, 0)

    WAIT_TIME = 20

    def __init__(self, maze, animate):
        """
        -maze: Maze object. Maze to be traversed. Stored in self.maze.
        -animate: Boolean. Determines whether pathfinding process will be shown.
            stored in self.animate.
        self.currentX: int. Represents algorithm's current column in the maze.
        self.currentY: int. Represents algorithm's current row in the maze.
        self.path: array. Represents all the nodes in the bath from the entrance
            to the exit."""
        self.maze = maze
        self.animate = animate

        self.currentX = maze.entrance.x
        self.currentY = maze.entrance.y
        self.path = []

        self.traverse()

        if not animate:
            maze.render()

    def traverse(self):
        """Continues maze wandering until the exit has been found.
        Changes current node's color to [CURRENT_COLOR], and then makes the next
        possible move."""

        move = self.moveRight

        while self.maze.grid[self.currentY][self.currentX] != self.maze.exit:

            self.changeNodeColor(self.maze.grid[self.currentY][self.currentX], self.CURRENT_COLOR)

            move = self.nextMove(move)
            move()

        self.createPath()

    def move(self):
        """Takes care of adding and removing coordinates (represented as tuples)
        from self.path.
        If a coordinate was already in self.path, it means that the algorithm is
        backtracking. In that case, remove that coordinate form self.path.
        Otherweise, it's a new node. Add to self.path."""

        current = (self.currentX, self.currentY)
        if current in self.path:
            self.path.pop()
        else:
            self.path.append(current)

        self.changeNodeColor(self.maze.grid[self.currentY][self.currentX], self.VISITED_COLOR, 0)

    def canMoveRight(self):
        """Checks if there is a path to the right."""

        if self.maze.grid[self.currentY][self.currentX + 1].isWall:
            return False
        return True

    def moveRight(self):
        """"Calls self.move and increments self.currentX"""

        self.move()
        self.currentX += 1

    def canMoveDown(self):
        """Checks if there is a path downwards."""

        if self.maze.grid[self.currentY + 1][self.currentX].isWall:
            return False
        return True

    def moveDown(self):
        """"Calls self.move and increments self.currentY"""

        self.move()
        self.currentY += 1

    def canMoveLeft(self):
        """Checks if there is a path to the left."""

        if self.maze.grid[self.currentY][self.currentX - 1].isWall:
            return False
        return True

    def moveLeft(self):
        """"Calls self.move and decrements self.currentX"""

        self.move()
        self.currentX -= 1

    def canMoveUp(self):
        """Checks if there is a path upwards."""

        if self.maze.grid[self.currentY - 1][self.currentX].isWall:
            return False
        return True

    def moveUp(self):
        """"Calls self.move and decrements self.currentY"""

        self.move()
        self.currentY -= 1

    def nextMove(self, move):
        """Finds the next possible move.
        -move: one of the above move functions. Represents the current direction
        in which the algorithm is moving.

        Depending on which direction the algorithm is currently moving, this
        function will return a move direction that prioritizes making right turns."""

        if move == self.moveDown:       #Algorithm is currently moving downwards
            if self.canMoveLeft():
                return self.moveLeft
            elif self.canMoveDown():
                return move
            elif self.canMoveRight():
                return self.moveRight
            return self.moveUp

        elif move == self.moveLeft:     #Algorithm is currently moving left
            if self.canMoveUp():
                return self.moveUp
            elif self.canMoveLeft():
                return move
            elif self.canMoveDown():
                return self.moveDown
            return self.moveRight

        elif move == self.moveUp:       #Algorithm is currently moving upwards
            if self.canMoveRight():
                return self.moveRight
            elif self.canMoveUp():
                return move
            elif self.canMoveLeft():
                return self.moveLeft
            return self.moveDown

        else:                           #Algorithm is currently moving right
            if self.canMoveDown():
                return self.moveDown
            elif self.canMoveRight():
                return move
            elif self.canMoveUp():
                return self.moveUp
            return self.moveLeft

    def createPath(self):
        """Renders the path from the entrance to the exit. Changes the color
        of all the nodes in self.path to PATH_COLOR."""

        for coord in self.path:
            self.changeNodeColor(self.maze.grid[coord[1]][coord[0]], self.PATH_COLOR, .5)
        self.changeNodeColor(self.maze.exit, self.PATH_COLOR, 0)

    def changeNodeColor(self, node, color, multiplier=1.0):
        """Changes the color of a node, and immediately renders it if animation
        is enabled (self.animate = True)
        -node: a Node object. The node whose color will be changed.
        -color: a pygame Color object. node's new color.
        -multiplier: double. Used to change WAIT_TIME in case a different effect
        is needed for different parts."""

        node.color = color
        if self.animate:
            node.render(self.maze.surface)
            if multiplier != 0:
                time.wait( int(self.WAIT_TIME * multiplier) )
        else:
            node.draw(self.maze.surface)

"""*****************************END OF HUGH-RIGHT-WALL****************************"""


"""*******************************A* SEARCH METHOD********************************"""
class A_Star:
    """A* pathfinding algorithm. Finds the shortest path to the exit by computing
    the cost of traversing through nodes and then taking the path of least expense.
    -PATH_COLOR: pygame Color object. Used for path from the entrance to the exit.
    -TO_VISIT_COLOR: pygame Color object. Used to show which nodes are in line to
        be evaluated. The one with the lowest cost is evaluated next.
    -VISITED_COLOR: pygame Color object. Used for visited nodes that are not in
        direct path from the entrance to the exit.
    -WAIT_TIME: int. The time (in ms) in between generation steps. Used to animate
    maze traversal."""

    PATH_COLOR = Color(0, 0, 200)
    TO_VISIT_COLOR = Color(255, 140, 0)
    VISITED_COLOR = Color(0, 200, 150)

    WAIT_TIME = 20

    class A_Node(Node):
        """Extends Node. Designed to meet A* pathfinding's need.
        -exit: Node object. Exit of the maze. Used by A_Nodes as reference to
            calculate h value."""

        exit = None

        #g -> distance from the start, h -> distance from the end, f -> g + h
        def __init__(self, current, parent=None):
            """
            -current: Node object. Node from Maze to be replaced.
            -parent: Node object. Node which minimizes f value."""

            if parent is None:
                self.g = 0
            else:
                self.g = parent.g + 1
            self.parent = parent
            Node.__init__(self, current.x, current.y, current.color)
            self.isWall = current.isWall

        @property
        def h(self):
            """h -> distance from node to the end."""
            return abs(self.exit.x - self.x) + abs(self.exit.y - self.y)

        @property
        def f(self):
            """f -> g + h."""
            return self.g + self.h

        def update(self, parent):
            """Updates g value and parent."""
            self.g = parent.g + 1
            self.parent = parent


    def __init__(self, maze, animate):
        """Initialization converts all nodes into A_Nodes, which contain special
        characteristics for this pathfinding algorithm
        -maze: Maze object. Stored in self.maze
        -animate: Boolean. Determines whether pathfinding process will be shown.
            stored in self.animate.
        """

        self.maze = maze
        self.animate = animate

        for row in range(maze.rows):
            for col in range(maze.cols):
                maze.grid[row][col] = self.A_Node(maze.grid[row][col])
        self.A_Node.exit = maze.grid[maze.exit.y][maze.exit.x]
        maze.entrance = maze.grid[maze.entrance.y][maze.entrance.x]

        self.generate()

        if not animate:
            maze.render()

    def generate(self):
        """Main logic of pathfinding algorithm. Evaluates nodes starting from
        the one with the lowest f value from self.toVisit. It then removes that
        node from self.toVisit and puts it in self.visited. If that node is not
        the exit, it then proceeds to queue all neighboring nodes for evaluation
        in the case they haven't been evaluated yet."""

        toVisit = [self.maze.entrance]
        visited = []

        while True:
            current = min(toVisit, key=lambda node: node.f)
            toVisit.remove(current)
            visited.append(current)
            self.changeNodeColor(current, self.VISITED_COLOR)

            if current is self.A_Node.exit:
                break

            for neighbor in self.getNeighbors(current):

                if neighbor in visited:
                    continue

                if neighbor.parent is None or neighbor.f > current.f + 1:

                    neighbor.update(current)

                    if neighbor not in toVisit:
                        toVisit.append(neighbor)
                        self.changeNodeColor(neighbor, self.TO_VISIT_COLOR)

        self.displayPath()

    def getNeighbors(self, node):
        """Gets all the neighbors of node"""

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
        """Checks if the right neighbor of node is not a wall and is not out of bounds"""

        if node.x == self.maze.cols - 1 or self.maze.grid[node.y][node.x + 1].isWall:
            return False
        return True

    def canMoveDown(self, node):
        """Checks if the top neighbor of node is not a wall"""

        if self.maze.grid[node.y + 1][node.x].isWall:
            return False
        return True

    def canMoveLeft(self, node):
        """Checks if the left neighbor of node is not a wall and is not out of bounds"""

        if node.x == 0 or self.maze.grid[node.y][node.x - 1].isWall:
            return False
        return True

    def canMoveUp(self, node):
        """Checks if the top neighbor of node is not a wall"""

        if self.maze.grid[node.y - 1][node.x].isWall:
            return False
        return True

    def displayPath(self):
        """Render path from the entrance to the exit. Rendering starts from the exit."""

        current = self.A_Node.exit
        while current is not None:
            self.changeNodeColor(current, self.PATH_COLOR, .5)
            current = current.parent

    def changeNodeColor(self, node, color, multiplier=1):
        """Changes the color of a node, and immediately renders it if animation
        is enabled (self.animate = True)
        -node: a Node object. The node whose color will be changed.
        -color: a pygame Color object. node's new color.
        -multiplier: double. Used to change WAIT_TIME in case a different effect
        is needed for different parts."""

        node.color = color
        if self.animate:
            node.render(self.maze.surface)
            if multiplier != 0:
                time.wait(int(self.WAIT_TIME * multiplier))
        else:
            node.draw(self.maze.surface)

"""***************************END A* PATHFINDING******************************"""
