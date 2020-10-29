# Maze Generation And Pathfinding

Python project that visualizes maze generation and multiple path-finding algorithms.

## How to use
Main program exectution is found in Driver.py. Press any button to step through program execution. After the maze has been solved, use the exit button to exit the program.<br />
`MAZE_WIDTH` and `MAZE_HEIGHT` are used to specify maze dimensions. Window size readjusts to fit any maze size. Mazes that are too big will go off-screen.<br />
`generate` and `solve` refer to the generation and pathfinding algorithms, respectively. To change algorithms, substitute the extension for the names described below.<br />
`animateGeneration` and `animateSolution` alter whether generation steps and pathfining steps will be shown. True -> show steps. False -> skip steps<br />

## Generation.py
### DepthFirst
Currently the only supported generation algorithm.<br />
Generates a path until there are no ways to go, then backtracks until it can create a different path.<br />
Mostly results in mazes with long, windy trails.<br />

![generation](/Assets/generationExample.png)

#### Color Key
  `gray`:   maze walls. Cursor cannot go through them<br />
  `white`:  maze halls. Cursor can move through them<br />
  `red`:    points the maze's entrance and exit<br />

## Pathfinding.py
### HugRightWall
As the name suggests, this algorithm works by prioritizing making right turns over anything else.<br />
It will often give the impression of wandering aimlessly... and it's pretty much doing that. It does not know where the exit is found, so it will go around until it finds it.<br />
Not super efficient and only works if all parts of the maze are connected by walls (no "islands").<br />

![HugRightWall](/Assets/hugRightWallPathfindingExample.png)

#### Color Key
  `orange`: algorithm's current position<br />
  `cyan`:   areas previously visited by the algorithm<br />
  `blue`:   shortest path from the entrance to the exit<br />
  
### A_Star
A* pathfinding algorithm.<br />
Works by stepping through the maze and moving through the path with the least cost. The cost of a path is determined by how far away it moves from the entrance, and how close to the exit it gets.<br />

![A_Star](/Assets/A_StarPathfindingExample.png)

#### Color Key
  `orange`: nodes in line to be evaluated. The one with the lowest cost is picked to be evaluated next<br />
  `cyan`:   nodes that have been evaluated<br />
  `blue`:   shortest path from the entrance to the exit<br />

## Dependencies
To run the program, you need to have `pygame` installed on your computer.<br />
To install, run `python3 -m pip install -U pygame --user`
