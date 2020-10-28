import pygame

class Node:
    """Node class handles each cell's rendering and drawing.
    -NODE_WIDTH: int. The width (in pixels) of all nodes."""

    NODE_WIDTH = 20

    def __init__(self, x, y, color):
        """
        -x: int. Represents column in which the node is found. Stored in self.x
        -y: int. Represents row in which the node is found. Stored in self.y
        -color: pygame Color object. Node's color.
        -self.visited: Boolean. Represents whether a node has been visited during
            generation.
        -self.isWall: Boolean. Represents whether a node is a wall."""

        self.x = x
        self.y = y
        self.color = color

        self.visited = False
        self.isWall = True

    def draw(self, surface):
        """Draws node into the screen. Does NOT render it. Node will be shown
        next time the display is updated. The location at which the node is drawn
        depends on it's x and y coordinates.
        -surface: pygame Surface object. Used to draw the node."""

        rectangle = pygame.Rect((self.x * Node.NODE_WIDTH, self.y * Node.NODE_WIDTH), (Node.NODE_WIDTH, Node.NODE_WIDTH))
        pygame.draw.rect(surface, self.color, rectangle)
        pygame.event.pump()

    def render(self, surface):
        """Draws the node and immediately renders it.
        -surface: pygame Surface object. Used to render."""

        self.draw(surface)
        pygame.display.update()

    def __str__(self):
        """String representation of Node. If it's a wall, node is represented by
        a '#'. If it's not. It is represented by a '.' (dot)."""
        if not self.isWall:
            return " . "
        return " # "
