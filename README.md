# Maze Generation And Pathfinding

Python project that visualizes maze generation and multiple path-finding algorithms.

## How to use
Main program exectution is found in Driver.py. Press any button to step through program execution. After the maze has been solved, use the exit button to exit the program.
`MAZE_WIDTH` and `MAZE_HEIGHT` are used to specify maze dimensions. Window size readjusts to fit any maze size. Mazes that are too big will go off-screen.
`generate` and `solve` refer to the generation and pathfinding algorithms, respectively. To change algorithms, substitute the extension for the names described below.
`animateGeneration` and `animateSolution` alter whether generation steps and pathfining steps will be shown. True -> show steps. False -> skip steps

## Generation.py
### DepthFirst
Currently the only supported generation algorithm. 
Generates a path until there are no ways to go, then backtracks until it can create a different path.
Mostly results in mazes with long, windy trails.

![Generation](/Assets/generationExample.png)

#### Color Key
  `gray`:   maze walls. Cursor cannot go through them
  `white`:  maze halls. Cursor can move through them
  `red`:    points the maze's entrance and exit

## Pathfinding.py
### HugRightWall
As the name suggests, this algorithm works by prioritizing making right turns over anything else.
It will often give the impression of wandering aimlessly... and it's pretty much doing that. It does not know where the exit is found, so it will go around until it finds it.
Not super efficient and only works if all parts of the maze are connected by walls (no "islands").
#### Color Key
  `orange`: algorithm's current position
  `cyan`:   areas previously visited by the algorithm
  `blue`:   shortest path from the entrance to the exit
  
### A_Star
A* pathfinding algorithm.
Works by calculating the cost of each node and traveling through the least expensive path.
#### Color Key
  `orange`: nodes in line to be evaluated. The one with the lowest cost is picked to be evaluated next
  `cyan`:   nodes that have been evaluated
  `blue`:   shortest path from the entrance to the exit

## Dependencies
To run the program, you need to have `pygame` installed on your computer.
To install, run `python3 -m pip install -U pygame --user`
