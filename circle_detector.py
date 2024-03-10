import cv2
from mss import mss
import numpy as np
import pyautogui
import time

# capture screen
def capture_screen(region=None):
    with mss() as sct:
        # take screenshot
        monitor = {"top": region[1], "left": region[0], "width": region[2], "height":region[3]} if region else sct.monitors[1]
        sct_img = sct.grab(monitor)
        # convert to a numpy array
        frame = np.array(sct_img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

# detect circles
def detect_circles(frame):
    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply gaussian blur
    gray = cv2.GaussianBlur(gray, (9, 9), 2)
    # detect circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    return circles

# main loop
while True:
    # screen region
    region = (640, 440, 1280, 720)
    frame = capture_screen(region=region)

    circles = detect_circles(frame)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle
            # move cursor to circle and click
            pyautogui.moveTo(x + region[0], y + region[1])
            pyautogui.click()
            # break test
            break
    # lil pause till next screen capture
    time.sleep(1)