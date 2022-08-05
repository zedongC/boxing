import cv2 as cv
import mediapipe as mp
import time
import HandTrackingModule
import math

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandTrackingModule.handDetector()
while True:
    success, img = cap.read()
    # Flip the image horizontally for a selfie-view display.
    img = cv.flip(img, 1)
    # 2.Find the hand landmarks
    img = detector.findHands(img)

    print(detector.handsNumber())
    if detector.handsNumber() == 1:
        detector.label(1)
    if detector.handsNumber() == 2:  # If we detect two hands
        detector.label(2)
        lmList = detector.findPosition(img, draw=False)
        print(lmList)
        # If both left and right hands get their respective data of positions
        if len(lmList[0]) != 0 and len(lmList[1]) != 0:

            x1, y1 = lmList[0][5][1], lmList[0][5][2]
            x2, y2 = lmList[0][17][1], lmList[0][17][2]
            x1_left, y1_left = lmList[1][5][1], lmList[1][5][2]
            x2_left, y2_left = lmList[1][17][1], lmList[1][17][2]

            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            distance_left = math.sqrt((x1_left - x2_left) ** 2 + (y1_left - y2_left) ** 2)
            print("left:",distance_left)
            print("right:",distance)

        # if distance > 150:
        #     print("Hit")

    cv.imshow('MediaPipe Hands', img)
    cv.waitKey(1)
