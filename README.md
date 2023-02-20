
# Water Sort Puzzle Solver

Solves "water sort puzzle" style games. One version, [SortPuz: Water Sort Puzzle](https://play.google.com/store/apps/details?id=sortpuz.water.sort.puzzle.game), can be played automatically.

## Dependencies

* PyGetWindow (https://github.com/asweigart/PyGetWindow)
* pyautogui (https://github.com/asweigart/pyautogui)
* opencv-python (https://github.com/opencv/opencv-python)

## Setup

1. Install python requirements from requirements.txt
2. Download scrcpy https://github.com/Genymobile/scrcpy/releases/
3. Enable debugging on your phone and 
4. 

## How it works

### Scanning the game state

1. Find the game window by window title
2. Move game window to preset location on main monitor
3. Screenshot window
4. Crop screenshot to only area of screen with tubes 
5. Threshold, binarize, and extract contours
6. Extract external countours to identify tubes
7. Crop image around each tube and 

### Finding a solution

#### Fully observable puzzles

For full observable puzzles, the problem is formulated as a search of a directed graph. Nodes represent combinations of colors in tubes. Nodes A and B are connected if a single valid pour (action) can transform A to B. The graph is expected to contain cycles.

The A* heuristic used is the number of boundaries between different colors in a tube. Search implementation adapted from [aimacode](https://github.com/aimacode).


#### Partially observable puzzles

Some puzzles contain layers marked with a '?'. When these '?' layers are exposed at the top of a tube, their true color is revealed. For these puzzles, until all the '?' layers are revlealed, the game state is only partially observable. The result is that immediately calculating an optimal solution is no longer possible. Partially observable puzzles can be modelled as Markov decision processes, since actions (pouring from one tube to another) have nondeterministic results.

### Executing moves

 