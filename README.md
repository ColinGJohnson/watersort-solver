
# Water Sort Puzzle Solver

Solves "water sort puzzle" style games.

#### Setup

1. Download scrcpy

### How it works

#### Scanning the game state

#### Finding a solution

The problem is formulated as a search of a directed graph. Nodes represent combinations of colors in tubes. Nodes A and B are connected if a single valid pour (action) can transform A to B. The graph is expected to contain cycles.

The A* heuristic used is the number of boundaries between different colors in a tube. The heuristic value 

Search implementation adapted from https://github.com/aimacode.

#### Executing moves