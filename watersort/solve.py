import time

from controller.SortPuzController import WaterSortController
from solver.WaterSortProblem import WaterSortProblem
from solver.WaterSortSolver import path_actions, weighted_astar_search, greedy_search, astar_search, uniform_cost_search

import argparse

solvers = {
    'weighted': weighted_astar_search,
    'astar': astar_search,
    'uniformcost': uniform_cost_search,
    'greedy': greedy_search
}


def main():
    parser = argparse.ArgumentParser(description='Solver for "sortpuz" water sort puzzle game.')
    parser.add_argument('window_title', type=str)
    parser.add_argument('-s', '--solver', choices=solvers.keys(), default='astar', help="Solver algorithm.")
    parser.add_argument('-l', '--layers', type=int, default=4, help="The number of color layers in each tube.")
    args = parser.parse_args()

    controller = WaterSortController(args.window_title, num_slices=args.layers)
    state = controller.update_state()
    print("Initial State:", state)

    problem = WaterSortProblem(4, state)
    solution_node = solvers[args.solver](problem)
    solution = path_actions(solution_node)
    print("Solution:", solution)

    for action in solution:
        controller.execute_action(action)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
