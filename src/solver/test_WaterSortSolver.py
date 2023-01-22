from pprint import pprint
from unittest import TestCase

from src.solver.WaterSortProblem import WaterSortProblem
from src.solver.WaterSortSolver import astar_search, path_states, path_actions


class Test(TestCase):
    def test_astar_search(self):
        problem = WaterSortProblem(4, [
            [0, 1, 1, 1],
            [1, 0, 2, 3],
            [0, 3, 0, 4],
            [5, 3, 4, 2],
            [5, 6, 2, 5],
            [3, 6, 4, 6],
            [2, 4, 6, 5],
            [],
            []
        ])
        goal_node = astar_search(problem)
        print(goal_node)
        print(path_actions(goal_node))
        # pprint(path_states(goal_node))
