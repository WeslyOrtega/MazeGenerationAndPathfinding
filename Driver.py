import pygame
import tkinter
from Node import Node

from Maze import Maze
import Generation
import Pathfinding

#Max number of recursive calls: 997
#Current Max Size = 61
MAZE_WIDTH = 71
MAZE_HEIGHT = 39

#Choose generation and pathfinding algorithms
generate = Generation.DepthFirst
solve = Pathfinding.A_Star

#Choose whether you want to see the animations
animateGeneration = False
animateSolution = True

#pygame screen handling
pygame.init()
screen = pygame.display.set_mode((Node.NODE_WIDTH * MAZE_WIDTH, Node.NODE_WIDTH * MAZE_HEIGHT))
pygame.display.set_caption("Maze Generation")

#pygame icon handling
icon = pygame.image.load("Assets/Icon.png")
pygame.display.set_icon(icon)


maze = Maze(MAZE_WIDTH, MAZE_HEIGHT, screen)    #Create Maze

#Wait for key to be pressed before starting generation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            generate(maze, animateGeneration)                  #Generate
            running = False
            break

#Wait for a key to be pressed before starting finding shortest path
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            solve(maze, animateSolution)
            running = False
            break

#Wait for a key to be pressed or exit button to be clicked to finish program
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False


    #maze.render()
