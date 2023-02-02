import unittest
from unittest import TestCase

from watersort.solver.WaterSortProblem import WaterSortProblem
from watersort.solver.WaterSortSolver import astar_search, path_actions, uniform_cost_search, greedy_search, \
    weighted_astar_search


class Test(TestCase):
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

    def test_weighted_astar_search(self):
        goal_node = weighted_astar_search(self.problem)
        actions = path_actions(goal_node)
        self.assertEqual(
            [(5, 7), (5, 8), (5, 7), (2, 8), (1, 5), (3, 1), (3, 8), (3, 5), (6, 3), (6, 7), (6, 8), (1, 6), (1, 2),
             (0, 1), (2, 0), (2, 5), (4, 3), (4, 6), (4, 7), (2, 0), (3, 4)],
            actions
        )

    def test_astar_search(self):
        goal_node = astar_search(self.problem)
        actions = path_actions(goal_node)
        self.assertEqual(
            [(5, 8), (5, 7), (5, 8), (1, 5), (3, 1), (3, 7), (3, 5), (4, 3), (6, 3), (6, 8), (6, 7), (1, 6), (2, 7),
             (1, 2), (4, 6), (0, 1), (2, 0), (2, 5), (4, 8), (4, 3), (0, 2)],
            actions
        )

    def test_greedy_search(self):
        goal_node = greedy_search(self.problem)
        actions = path_actions(goal_node)
        self.assertEqual(
            [(0, 7), (3, 8), (2, 3), (2, 0), (1, 2), (1, 8), (1, 0), (1, 7), (3, 1), (3, 2), (6, 3), (5, 6), (4, 3),
             (5, 1), (6, 5), (6, 1), (4, 6), (6, 8), (4, 6), (5, 6), (2, 5), (2, 0), (3, 4)],
            actions
        )

    @unittest.skip("Disabled due to long runtime.")
    def test_uniform_cost_search(self):
        goal_node = uniform_cost_search(self.problem)
        print(goal_node)
        print(path_actions(goal_node))
        print("actions used:", len(path_actions(goal_node)))
