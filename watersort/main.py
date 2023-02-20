import time

from controller.WaterSortController import WaterSortController
from solver.WaterSortProblem import WaterSortProblem
from solver.WaterSortSolver import path_actions, weighted_astar_search, greedy_search

import argparse


def main():
    parser = argparse.ArgumentParser(description='Solver for "sortpuz" water sort puzzle game.')

    parser.add_argument('window title', type=str)
    parser.add_argument('-s', '--solver', choices=['weighted', 'astar', 'uniformcost', 'greedy'], default='astar')

    args = parser.parse_args()

    controller = WaterSortController(args.window_title)
    state = controller.update_state()
    print("Initial State:", state)

    problem = WaterSortProblem(4, state)
    solution = path_actions(greedy_search(problem))
    print("Solution:", solution)

    for action in solution:
        controller.execute_action(action)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
