import cv2 as cv
import HandTrackingModule
import os
import math
import numpy as np
import time
import pyautogui as autopy


wCam, hCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

wScr, hScr = autopy.size()  # Width and height of the screen
frameR = 100
detector = HandTrackingModule.handDetector()
while True:
    success, img = cap.read()

    # 1. Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    cv.rectangle(img, (frameR, frameR),(wCam - frameR, hCam - frameR), (0, 255, 0), 2)
    if len(lmList) != 0:
        # Tip for the index finger
        x1, y1 = lmList[8][1:]
        # Tip for the middle finger
        x2, y2 = lmList[12][1:]

        cv.circle(img, (x1, y1), 10, (200, 100, 0), cv.FILLED)
        distance = math.hypot(x2 - x1, y2 - y1)
        if distance < 100:
            cv.circle(img, (x2, y2), 10, (200, 100, 0), cv.FILLED)
        # 5. Convert coordinates
        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, wCam - frameR), (0, wScr))

        # 6. Smoothen values
        # 7. Move the mouse
        autopy.moveTo(wScr - x3, hScr - y3)  # Flip the position
        distance = math.hypot(x2 - x1, y2 - y1)  # The distance between index and middle fingers
        # 3.Check the mode
        if distance < 50:  # Click mode
            cv.circle(img, (x2, y2), 10, (0, 125, 0), cv.FILLED)
        #else:




    cv.imshow("Image", img)
    cv.waitKey(1)
