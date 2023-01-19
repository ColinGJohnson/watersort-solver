from unittest import TestCase
from WaterSortProblem import WaterSortProblem, is_complete


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
        self.assertFalse(is_complete([[1, 2, 3], [3, 4, 5]]))

    def test_get_actions(self):
        pass

    def test_can_pour(self):
        pass

    def test_pour(self):
        pass
