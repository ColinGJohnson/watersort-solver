from pprint import pprint
from typing import List

import colour
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import pygetwindow as gw
from PIL import Image
from numpy._typing import ArrayLike


def screenshot_window(window_title: str) -> Image:
    window = gw.getWindowsWithTitle(window_title)[0]
    window.restore()
    window.activate()
    window.moveTo(10, 10)
    region = (window.left, window.top, window.width, window.height)
    return pyautogui.screenshot(region=region)


def plot(img_plt):
    img_rgb = cv.cvtColor(img_plt, cv.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.rcParams["figure.figsize"] = (20, 20)
    plt.show()


def draw_and_wait(draw_img):
    cv.imshow('image', draw_img)
    cv.waitKey(0)


# screenshot = screenshot_window('Pixel 7 Pro')
# screenshot.save(f'test.png')
# screenshot.show()

# img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
# cv.imshow('image', opencvImage)
# cv.waitKey(0)

do_debug_draw = False

screenshot_img = cv.imread('test.png')
print(screenshot_img.shape, screenshot_img.dtype)

top_left = (int(screenshot_img.shape[1] * 0.05), int(screenshot_img.shape[0] * 0.3))
bottom_right = (int(screenshot_img.shape[1] * 0.95), int(screenshot_img.shape[0] * 0.8))

if do_debug_draw:
    img_annotated = screenshot_img.copy()
    rectangle_color = (0, 255, 0)
    cv.rectangle(img_annotated, top_left, bottom_right, rectangle_color, 3)
    draw_and_wait(img_annotated)


def find_tubes(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, img_thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(img_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    locations = []

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        locations.append((x, y, w, h))

    if do_debug_draw:
        img_drawn_contours = cv.cvtColor(img_thresh, cv.COLOR_GRAY2BGR)
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img_drawn_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.drawContours(img_drawn_contours, contours, -1, (255, 0, 255), 2)
        plot(img_drawn_contours)

    return locations


img_cropped = screenshot_img.copy()[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
tube_locations = find_tubes(img_cropped)

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

num_slices = 4
offset_proportion = 0.15
bg_color = cv.cvtColor(img_cropped.astype(np.float32) / 255, cv.COLOR_BGR2Lab)[0, 0]
color_palette = [bg_color]
tubes = []
for tube in tube_locations:
    x, y, w, h = tube
    tube_crop = img_cropped[y:y + h, x:x + w]

    # convert to lab to make it easier to compare colors
    tube_crop_lab = cv.cvtColor(tube_crop.astype(np.float32) / 255, cv.COLOR_BGR2Lab)
    offset = offset_proportion * h
    slice_height = (h - offset) / num_slices
    # plot(tube_crop)

    print("\n", tube)
    tube = []
    for i in range(num_slices):
        slice_top = offset + (slice_height * i)

        sample_y = int(slice_top + slice_height / 2)
        sample_x = int(w / 2)
        color_sample = tube_crop[sample_y, sample_x]
        color_sample_lab = tube_crop_lab[sample_y, sample_x]

        print("color:", i, color_sample)
        print("lab:", color_sample_lab)
        sample_index = add_sample_to_palette(color_palette, color_sample_lab)
        print("Added as ", sample_index)

        img_pos = (top_left[0] + x + sample_x, top_left[1] + y + sample_y)
        cv.drawMarker(screenshot_img, img_pos, (0, 255, 0), 2)
        cv.putText(screenshot_img, str(sample_index), img_pos, cv.QT_FONT_NORMAL, 1, (255, 255, 255), 2, cv.LINE_AA)

        tube.append({'colors': sample_index, 'positions': img_pos})

    tubes.append(((x, y), tube))

pprint(tubes)

plot(img_cropped)
plot(screenshot_img)
