from datetime import time
from pprint import pprint
from typing import List, Tuple

import colour
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import pygetwindow as gw
from PIL import Image
from numpy._typing import ArrayLike

from solver.WaterSortTypes import Action


def show_img(img_plt):
    img_rgb = cv.cvtColor(img_plt, cv.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.rcParams["figure.figsize"] = (20, 20)
    plt.show()


def draw_and_wait(draw_img):
    cv.imshow('image', draw_img)
    cv.waitKey(0)


def find_tube_locations(img, debug=False) -> List[Tuple[int, int, int, int]]:
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img_thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(img_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    locations = []

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        locations.append((x, y, w, h))

    if debug:
        img_drawn_contours = cv.cvtColor(img_thresh, cv.COLOR_GRAY2BGR)
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img_drawn_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.drawContours(img_drawn_contours, contours, -1, (255, 0, 255), 2)
        show_img(img_drawn_contours)

    return locations


def crop_img(img, left_crop=0.05, right_crop=0.05, top_crop=0.3, bottom_crop=0.2):
    left = int(img.shape[1] * left_crop)
    right = int(img.shape[1] * 1 - right_crop)
    top = int(img.shape[0] * top_crop)
    bottom = int(img.shape[0] * 1 - bottom_crop)
    return top, left, img.copy()[top:bottom, left:right]


def add_sample_to_palette(palette: List[ArrayLike], color: ArrayLike):
    """Adds a color to a set if it isn't similar enough to one already in the set. Colors are compared using the
    CIE 2000 definition of color difference (https://en.wikipedia.org/wiki/Color_difference). Parameters are expected
    to be colors in the Lab color space and provided as numpy arrays [L, a, b]."""

    delta_e_threshold = 5

    for i, palette_color in enumerate(palette):
        delta_e = colour.delta_E(palette_color, color)
        if delta_e < delta_e_threshold:
            print("Found existing color in palette:", i, delta_e, color, palette_color)
            return i

    print("adding new color to palette:", color)
    palette.append(color)
    return len(palette) - 1


class WaterSortController:
    """Abstracts actions in the 'SortPuz' app."""

    num_slices = 4
    offset_proportion = 0.15

    def __init__(self, window_title: str):
        self.window = gw.getWindowsWithTitle(window_title)[0]

    def restore_window(self):
        """Moves the game window to a standard location on the main monitor. Main monitor is needed
        because screenshots don't work on secondary monitors."""
        self.window.restore()
        self.window.activate()
        self.window.moveTo(10, 10)

    def screenshot_window(self) -> Image:
        self.restore_window()
        region = (self.window.left, self.window.top, self.window.width, self.window.height)
        return cv.cvtColor(np.array(pyautogui.screenshot(region=region)), cv.COLOR_RGB2BGR)

    def update_state(self, debug=True):
        """Screenshot the window and apply image processing to determine the current game state"""

        img_screenshot = self.screenshot_window()
        top, left, img_cropped = crop_img(img_screenshot)

        # assume the game's background color is similar to the pixel at the top right of the cropped screenshot
        bg_color = cv.cvtColor(img_cropped.astype(np.float32) / 255, cv.COLOR_BGR2Lab)[0, 0]
        color_palette = [bg_color]

        tube_locations = find_tube_locations(img_cropped)
        tubes = []

        for tube_location in tube_locations:
            print("Checking tube at location (offset from cropped):", tube_location)
            x, y, w, h = tube_location
            tube_crop = img_cropped[y:y + h, x:x + w]
            tubes.append({
                'tube_location': tube_location,
                'layers': self.read_tube_layer_colors(color_palette, tube_crop)
            })

        for tube in tubes:
            x, y, w, h = tube['tube_location']
            for layer in tube['layers']:
                sample_x, sample_y = layer.get('tube_position_xy')
                layer['crop_position'] = (left + x + sample_x, top + y + sample_y)
                if debug:
                    color = str(layer.get('color'))
                    cv.drawMarker(img_screenshot, layer['crop_position'], (0, 255, 0), 2)
                    cv.putText(img_screenshot, color, layer['crop_position'], cv.QT_FONT_NORMAL, 1, (255, 255, 255), 2, cv.LINE_AA)
        if debug:
            pprint(tubes)
            show_img(img_cropped)
            show_img(img_screenshot)

        return tubes

    def read_tube_layer_colors(self, color_palette, tube_crop):
        h, w, _ = tube_crop.shape
        tube_crop_lab = cv.cvtColor(tube_crop.astype(np.float32) / 255, cv.COLOR_BGR2Lab)
        offset = self.offset_proportion * h
        slice_height = (h - offset) / self.num_slices

        layers = []
        for i in range(self.num_slices):
            sample_y = int(offset + (slice_height * i) + (slice_height / 2))
            sample_x = int(w / 2)
            color_sample_lab = tube_crop_lab[sample_y, sample_x]
            sample_index = add_sample_to_palette(color_palette, color_sample_lab)
            layers.append({
                'color_lab': color_sample_lab,
                'color_index': sample_index,
                'tube_position_xy': (sample_x, sample_y)
            })

        return layers

    def execute_action(self, action: Action):
        pass

    def click_window_location(self, target: Tuple[int, int]):
        monitor_x = self.window.left + target[0]
        monitor_y = self.window.top + target[1]
        pyautogui.moveTo(monitor_x, monitor_y, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
