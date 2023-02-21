
# Water Sort Puzzle Solver

Solves "water sort puzzle" style games. One version, [SortPuz: Water Sort Puzzle](https://play.google.com/store/apps/details?id=sortpuz.water.sort.puzzle.game), can be played automatically.

## Dependencies

* [scrcpy](https://github.com/Genymobile/scrcpy) for controlling SortPuz on an android device via USB debugging
* [PyGetWindow](https://github.com/asweigart/PyGetWindow) for obtaining the position of the scrpy window
* [opencv-python](https://github.com/opencv/opencv-python) for image processing to determine game state.
* [pyautogui](https://github.com/asweigart/pyautogui) for executing solutions.


## Setup

1. Install python requirements from [requirements.txt](requirements.txt)
2. [Download scrcpy](https://github.com/Genymobile/scrcpy/releases/)
3. [Enable USB debugging](https://developer.android.com/studio/debug/dev-options#Enable-debugging) on your phone and start scrcpy
4. Open SortPuz on the connected android device and open a puzzle
5. Run the solver e.g. `python3 solve.py "Pixel 7 Pro" --solver=greedy`

### Usage
```
usage: solve.py [-h] [-s {weighted,astar,uniformcost,greedy}] [-l LAYERS]
                window_title

Solver for "sortpuz" water sort puzzle game.

positional arguments:
  window_title

options:
  -h, --help            show this help message and exit
  -s {weighted,astar,uniformcost,greedy}, --solver {weighted,astar,uniformcost,greedy}
                        Solver algorithm.
  -l LAYERS, --layers LAYERS
                        The number of color layers in each tube.
```

## How it Works

### Scanning the game state

The current game state is obtained by processing a screenshot of an open scrcpy window. The number of tubes, as well as their 

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

Note: Partially observable puzzles are not yet implemented.

Some puzzles contain layers marked with a '?'. When these '?' layers are exposed at the top of a tube, their true color is revealed. For these puzzles, until all the '?' layers are revealed, the game state is only partially observable. The result is that immediately calculating an optimal solution, as is done for "fully observable" puzzles, is no longer possible. Partially observable puzzles can be modelled as Markov decision processes, since actions (pouring from one tube to another) have nondeterministic results.

### Executing moves

While scanning the game state, the location of each of the tubes on the screen are recorded. To execute a solution, pyautogui is used to click the correct sequence of tubes. The game state is not checked after each action, so moving the mouse or the scrcpy window during these moves will cause issues.