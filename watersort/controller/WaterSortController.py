import time
from typing import List, Tuple

import colour
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import pygetwindow as gw
from numpy._typing import ArrayLike, NDArray

from solver.WaterSortTypes import Action, GameState


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


def crop_img(img, left_crop=0.05, right_crop=0.05, top_crop=0.3, bottom_crop=0.2) -> Tuple[int, int, NDArray]:
    """Trim the edges of the input image by the specified proportions. The defaults are the values that
    happened to work well for my phone (Pixel 7 Pro)."""

    left = int(img.shape[1] * left_crop)
    right = int(img.shape[1] * (1 - right_crop))
    top = int(img.shape[0] * top_crop)
    bottom = int(img.shape[0] * (1 - bottom_crop))
    return top, left, img.copy()[top:bottom, left:right]


def add_sample_to_palette(palette: List[ArrayLike], color: ArrayLike):
    """Adds a color to a set if it isn't similar enough to one already in the set. Colors are compared using the
    CIE 2000 definition of color difference (https://en.wikipedia.org/wiki/Color_difference). Parameters are expected
    to be colors in the Lab color space and provided as numpy arrays [L, a, b]."""

    delta_e_threshold = 5

    for i, palette_color in enumerate(palette):
        delta_e = colour.delta_E(palette_color, color)
        if delta_e < delta_e_threshold:
            return i

    palette.append(color)
    return len(palette) - 1


class WaterSortController:
    """Abstracts actions in the 'SortPuz' app."""

    offset_proportion = 0.15
    window_position = {'x': 40, 'y': 10}

    def __init__(self, window_title: str, num_slices=4):
        self.controller_state = None
        self.num_slices = num_slices
        self.window = gw.getWindowsWithTitle(window_title)[0]

    def restore_window(self):
        """Moves the game window to a standard location on the main monitor. Main monitor is needed
        because screenshots don't work on secondary monitors."""
        self.window.restore()
        self.window.activate()
        self.window.moveTo(self.window_position['x'], self.window_position['y'])

    def screenshot_window(self) -> NDArray:
        self.restore_window()
        region = (self.window.left, self.window.top, self.window.width, self.window.height)
        return cv.cvtColor(np.array(pyautogui.screenshot(region=region)), cv.COLOR_RGB2BGR)

    def update_state(self, debug=True) -> GameState:
        """Screenshot the window and apply image processing to determine the current game state"""

        img_screenshot = self.screenshot_window()
        top, left, img_cropped = crop_img(img_screenshot)

        # assume the game's background color is similar to the pixel at the top right of the cropped screenshot
        bg_color = cv.cvtColor(img_cropped.astype(np.float32) / 255, cv.COLOR_BGR2Lab)[0, 0]

        # color index '0' will always represent the background color, so we can filter out empty layers
        color_palette = [bg_color]

        tube_locations = find_tube_locations(img_cropped)
        tubes = []

        for tube_location in tube_locations:
            x, y, w, h = tube_location
            tube_crop = img_cropped[y:y + h, x:x + w]
            tubes.append({
                'tube_location': tube_location,
                'layers': self.read_tube_layer_colors(color_palette, tube_crop)
            })

        for tube in tubes:
            x, y, w, h = tube['tube_location']

            if debug:
                cv.rectangle(img_cropped, (x, y), (x + w, y + h), (255, 0, 255), 2)

            for layer in tube['layers']:
                sample_x, sample_y = layer.get('tube_position_xy')

                # position relative to cropped area
                layer['crop_position'] = (x + sample_x, y + sample_y)

                # position relative to scrcpy window
                layer['window_position'] = (left + layer['crop_position'][0], top + layer['crop_position'][1])

                # position relative to main monitor.
                # TODO: Not currently used by click_window_location, this can be removed
                layer['monitor_position'] = (
                    self.window_position['x'] + layer['crop_position'][0],
                    self.window_position['y'] + layer['crop_position'][1]
                )

                if debug:
                    color = str(layer.get('color_index'))
                    cv.drawMarker(img_cropped, layer['crop_position'], (0, 255, 0), 2)
                    cv.putText(img_cropped, color, layer['crop_position'], cv.QT_FONT_NORMAL, 1, (255, 255, 255), 2, cv.LINE_AA)

        if debug:
            show_img(img_cropped)

        self.controller_state = tubes

        # convert the internal state used by the controller to a state usable by the solver
        layers = [[layer.get('color_index') for layer in tube.get('layers')] for tube in tubes]
        return [list(filter(lambda idx: idx != 0, layer))[::-1] for layer in layers]

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
        source_index, sink_index = action

        source_location = self.controller_state[source_index]['layers'][0]['window_position']
        self.click_window_location((source_location[0], source_location[1]))

        time.sleep(0.1)

        sink_location = self.controller_state[sink_index]['layers'][0]['window_position']
        self.click_window_location((sink_location[0], sink_location[1]))

    def click_window_location(self, target: Tuple[int, int]):
        monitor_x = self.window.left + target[0]
        monitor_y = self.window.top + target[1]
        pyautogui.moveTo(monitor_x, monitor_y, duration=0.2, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
