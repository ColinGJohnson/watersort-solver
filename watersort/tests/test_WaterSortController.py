import time
from unittest import TestCase

from controller.WaterSortController import WaterSortController
from solver.WaterSortProblem import WaterSortProblem
from solver.WaterSortSolver import greedy_search, path_actions


class TestWaterSortController(TestCase):
    def test_update_state(self):
        controller = WaterSortController('Test')
        state = controller.parse_screenshot()
        print(state)

