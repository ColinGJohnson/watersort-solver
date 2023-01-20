from unittest import TestCase
from WaterSortProblem import WaterSortProblem, is_complete, pour


class TestWaterSortProblem(TestCase):
    def test_is_complete(self):
        # Complete
        self.assertTrue(is_complete([]))
        self.assertTrue(is_complete([[]]))
        self.assertTrue(is_complete([[], []]))
        self.assertTrue(is_complete([[1], [2]]))
        self.assertTrue(is_complete([[1, 1], [2], [3, 3, 3]]))

        # Incomplete
        self.assertFalse(is_complete([[1, 2]]))
        self.assertFalse(is_complete([[3], [1, 1, 2]]))
        self.assertFalse(is_complete([[2, 1, 1], [3]]))
        self.assertFalse(is_complete([[1, 2, 3], [3, 4, 5], [6, 6, 6]]))

    def test_pour(self):
        self.assertListEqual(
            pour([[1], []], (0, 1)),
            [[], [1]]
        ),
        self.assertListEqual(
            pour([[1], []], (1, 0)),
            [[1], []]
        ),
        self.assertListEqual(
            pour([[], [2]], (1, 0)),
            [[2], []]
        ),
        self.assertListEqual(
            pour([[1, 2, 3], [], [3, 3]], (2, 0)),
            [[1, 2, 3, 3], [], [3]]
        ),
        self.assertListEqual(
            pour([[3, 3, 3], [1], [2], [3]], (0, 3)),
            [[3, 3], [1], [2], [3, 3]]
        ),

    def test_can_pour(self):
        pass

    def test_num_boundaries(self):
        pass

    def test_get_actions(self):
        pass
