import os
from unittest import TestCase

import cv2 as cv
from controller.WaterSortController import WaterSortController


class TestWaterSortController(TestCase):

    def test_parse_screenshot(self):
        controller = WaterSortController('Test')
        print(os.getcwd())
        test_image = cv.imread('resources/test_screenshot.png', cv.IMREAD_COLOR)
        state = controller.parse_screenshot(test_image, debug=False)
        self.assertEqual(
            [[], [], [3, 1, 2, 1], [5, 2, 4, 4], [4, 5, 5, 3], [3, 3, 6, 5], [1, 7, 4, 6], [7, 6, 6, 1], [2, 2, 7, 7]],
            state
        )
