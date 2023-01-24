import time

import cv2 as cv
import numpy as np
import pyautogui
import pygetwindow as gw
from PIL import Image


def screenshot_window(window_title: str) -> Image:
    window = gw.getWindowsWithTitle(window_title)[0]
    window.restore()
    window.activate()
    window.moveTo(10, 10)
    region = (window.left, window.top, window.width, window.height)
    return pyautogui.screenshot(region=region)


# screenshot = screenshot_window('Pixel 7 Pro')
# screenshot.save(f'test.png')
# screenshot.show()
#
# img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
# cv.imshow('image', opencvImage)
# cv.waitKey(0)

img = cv.imread('test.png')
print(img.shape, img.dtype)

top_left = (int(img.shape[1] * 0.05), int(img.shape[0] * 0.3))
bottom_right = (int(img.shape[1] * 0.95), int(img.shape[0] * 0.8))

img_annotated = img.copy()
rectangle_color = (0, 255, 0)
cv.rectangle(img_annotated, top_left, bottom_right, rectangle_color, 3)
cv.imshow('image', img_annotated)
cv.waitKey(0)

img_tubes = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
cv.imshow('image', img_tubes)
cv.waitKey(0)

img_gray = cv.cvtColor(img_tubes, cv.COLOR_BGR2GRAY)
cv.imshow('image', img_gray)
cv.waitKey(0)

_, img_thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imshow('image', img_thresh)
cv.waitKey(0)

contours, hierarchy = cv.findContours(img_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
print(len(contours), " tubes found")
# print("hierarchy", hierarchy.shape, hierarchy)
# print("contours", contours)

img_drawn_contours = cv.cvtColor(img_thresh, cv.COLOR_GRAY2BGR)
for contour in contours:
    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(img_drawn_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv.drawContours(img_drawn_contours, contours, -1, (255, 0, 255), 2)

cv.imshow('image', img_drawn_contours)
cv.waitKey(0)
