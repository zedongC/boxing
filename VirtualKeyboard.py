import cv2 as cv
import numpy as np
import HandTrackingModule
import math
from time import sleep

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandTrackingModule.handDetector(detectionCon=0.8)


class Button():
    def __init__(self, pos, text, size=80):
        self.pos = pos
        self.text = text
        self.size = size


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        size = button.size
        cv.rectangle(img, (x, y), (x + size, y + size), (255, 0, 255), cv.FILLED)

        cv.putText(img, button.text, (x + 13, y + 65), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    # The input rectangle
    cv.rectangle(img, (50, 360), (1030, 460), (255, 0, 255), cv.FILLED)
    # If the user inputs
    if len(input) != 0:
        xStart = 60
        for text in input:
            cv.putText(img, text, (xStart, 420), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            xStart += 60
    return img


keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Creating button objects out of the loop, so we can just call the draw method in the loop, which requires less work
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
input = []

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    # 2.Find the hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    img = drawAll(img, buttonList)

    if len(lmList) != 0:
        for button in buttonList:
            x, y = button.pos
            size = button.size
            midX, midY = lmList[12][1], lmList[12][2]
            indexX, indexY = lmList[8][1], lmList[8][2]
            # If choose a key, Bigger and darker
            if x < midX < x + size and y < midY < y + size:
                cv.rectangle(img, (x - 5, y - 5), (x + size + 5, y + size + 5), (175, 0, 175), cv.FILLED)
                cv.putText(img, button.text, (x + 5, y + 75), cv.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 5)
                # If click, color changes
                if abs(midX - indexX) < 30 and abs(midY - indexY) < 30:
                    cv.rectangle(img, (x - 5, y - 5), (x + size + 5, y + size + 5), (255, 0, 105), cv.FILLED)
                    cv.putText(img, button.text, (x + 5, y + 75), cv.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 5)
                    input.append(button.text)
                    sleep(0.1)  # Easy way but still not safe, sleep so the loop will not execute again that quickly

    cv.imshow("Image", img)
    cv.waitKey(1)
