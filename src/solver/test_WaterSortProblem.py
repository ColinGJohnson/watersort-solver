from unittest import TestCase

from WaterSortProblem import is_complete, pour, can_pour, num_boundaries, get_actions


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
            pour(4, [[1], []], (0, 1)),
            [[], [1]]
        ),
        self.assertListEqual(
            pour(4, [[2], []], (1, 0)),
            [[2], []]
        ),
        self.assertListEqual(
            pour(4, [[1, 2, 3], [], [3, 3]], (2, 0)),
            [[1, 2, 3, 3], [], [3]]
        ),

        # When a multiple of the same color are stacked, they are all poured
        self.assertListEqual(
            pour(4, [[3, 3, 3], []], (0, 1)),
            [[], [3, 3, 3]]
        ),

        # When there's limited capacity, only part of a group of color is poured
        self.assertListEqual(
            pour(3, [[3, 3], [1, 2]], (0, 1)),
            [[3], [1, 2, 3]]
        ),

    def test_can_pour(self):
        # Tube capacity must be >= 1
        self.assertRaises(ValueError, lambda: can_pour(0, [1], []))

        # Can't pour empty tube
        self.assertFalse(can_pour(4, [], [1]))

        # Can't pour into tube that is full
        self.assertFalse(can_pour(4, [1], [1, 1, 1, 1]))

        # Can't pour one color onto a different color
        self.assertFalse(can_pour(4, [2], [1]))

        # Pour into empty tube
        self.assertTrue(can_pour(4, [1], []))

        # Pour onto same color
        self.assertTrue(can_pour(4, [1], [1, 1, 1]))

    def test_num_boundaries(self):
        # Empty puzzle
        self.assertEqual(num_boundaries([]), 0)

        # Single tube
        self.assertEqual(num_boundaries([[]]), 0)
        self.assertEqual(num_boundaries([[1]]), 0)
        self.assertEqual(num_boundaries([[1, 2]]), 1)
        self.assertEqual(num_boundaries([[1, 2, 1]]), 2)
        self.assertEqual(num_boundaries([[1, 2, 3]]), 2)
        self.assertEqual(num_boundaries([[1, 2, 3, 4]]), 3)

        # Multiple tubes
        self.assertEqual(num_boundaries([[], []]), 0)
        self.assertEqual(num_boundaries([[1], [1]]), 0)
        self.assertEqual(num_boundaries([[1], [1, 2], []]), 1)
        self.assertEqual(num_boundaries([[1, 2, 3, 4], [1, 2, 2], [5, 5, 5]]), 4)

    def test_get_actions(self):

        # There are no valid actions when there are no colors in the tubes
        self.assertSetEqual(set(), get_actions(4, []))
        self.assertSetEqual(set(), get_actions(4, [[]]))
        self.assertSetEqual(set(), get_actions(4, [[], []]))

        # Tubes cannot be poured if there is no space
        self.assertSetEqual(set(), get_actions(1, [[1], [1]]))
        self.assertSetEqual(set(), get_actions(2, [[2, 1], [1, 1]]))

        # Tubes cannot be poured onto the wrong color
        self.assertSetEqual(set(), get_actions(3, [[1, 1], [2, 2]]))
        self.assertSetEqual(set(), get_actions(4, [[1], [2], [3], [4]]))

        # You can always pour into an empty tube
        self.assertSetEqual({(0, 1)}, get_actions(4, [[1], []]))
        self.assertSetEqual({(0, 1)}, get_actions(4, [[1, 2, 2, 2], []]))

        # Multiple tubes to pour into
        self.assertSetEqual({(1, 2), (1, 0)}, get_actions(4, [[], [1], []]))
        self.assertSetEqual({(0, 2), (0, 1)}, get_actions(4, [[1, 2, 2, 2], [], []]))

        # Multiple tube to pour from
        self.assertSetEqual({(0, 2), (1, 2)}, get_actions(2, [[1, 1], [1, 1], []]))
