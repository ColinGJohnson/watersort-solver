import time
from pprint import pprint

from controller.WaterSortController import WaterSortController
from solver.WaterSortProblem import WaterSortProblem
from solver.WaterSortSolver import weighted_astar_search, path_actions


def main():
    controller = WaterSortController('Pixel 7 Pro')
    state = controller.update_state()
    print("Initial State:", state)

    problem = WaterSortProblem(4, state)
    solution = path_actions(weighted_astar_search(problem))
    print("Solution:", solution)

    for action in solution:
        controller.execute_action(action)
        time.sleep(1)


if __name__ == "__main__":
    main()
