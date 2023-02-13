
# Water Sort Puzzle Solver

Solves "water sort puzzle" style games.

## Dependencies

* PyGetWindow (https://github.com/asweigart/PyGetWindow)
* pyautogui (https://github.com/asweigart/pyautogui)
* opencv-python (https://github.com/opencv/opencv-python)

## Setup

1. Download scrcpy https://github.com/Genymobile/scrcpy/releases/tag/v1.25

## How it works

## Scanning the game state

1. Find the game window by window title
2. Move game window to preset location on main monitor
3. Screenshot window
4. Crop screenshot to only area of screen with tubes 
5. Threshold, binarize, and extract contours
6. Extract external countours to identify tubes
7. Crop image around each tube and 

## Finding a solution

### Fully observable puzzles

For full observable puzzles, the problem is formulated as a search of a directed graph. Nodes represent combinations of colors in tubes. Nodes A and B are connected if a single valid pour (action) can transform A to B. The graph is expected to contain cycles.

The A* heuristic used is the number of boundaries between different colors in a tube. Search implementation adapted from [aimacode](https://github.com/aimacode).


### Partially observable puzzles

Partially observable puzzles can be modelled as Markov decision processes, since actions (pouring from one tube to another) 

## Executing moves

 