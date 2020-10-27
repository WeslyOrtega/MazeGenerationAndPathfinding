import pygame

class Node:

    NODE_WIDTH = 20

    def __init__(self, x, y, color):
        self.visited = False
        self.isWall = True

        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        rectangle = pygame.Rect((self.x * Node.NODE_WIDTH, self.y * Node.NODE_WIDTH), (Node.NODE_WIDTH, Node.NODE_WIDTH))
        pygame.draw.rect(surface, self.color, rectangle)

    def render(self, surface):
        self.draw(surface)
        pygame.display.update()
        pygame.event.pump()

    def changeColor(self, color):
        self.color = color

    def __str__(self):
        if not self.isWall:
            return " . "
        return " # "
