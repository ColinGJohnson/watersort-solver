import os
import time

import PIL
import pyautogui
import pygetwindow
import pygetwindow as gw

# pyautogui.moveTo(300, 300)
# print(gw.getAllTitles())

phone_window_title = 'Pixel 7 Pro'
phone_window = gw.getWindowsWithTitle(phone_window_title)[0]
phone_window.restore()


def screenshot_window(window: pygetwindow.Win32Window):

    window.activate()
    time.sleep(1)
    region = (window.left, window.top, window.width, window.height)
    print(region)
    # screenshot = pyautogui.screenshot(region=region)
    screenshot = pyautogui.screenshot(region=(2663, 0, 650, 1343))
    screenshot.save(f'test-{int(time.time())}.png')


screenshot_window(phone_window)
