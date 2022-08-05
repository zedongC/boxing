import cmath

import cv2 as cv
import HandTrackingModule
import math

def volumeChange(pts1, pts2, mid):
    volume = 100
    distance = math.sqrt((pts1[0] - pts2[0]) ** 2 + (pts2[1] - pts1[1]) ** 2)
    print(distance)

    maxLen = 240
    minLen = 20
    if distance < minLen:
        volume = 0
        cv.circle(img, (int(midX), int(midY)), 8, (0, 255, 0), cv.FILLED)  # Mid point
    elif distance < maxLen:
      volume = int(distance / 280 * volume)
      cv.circle(img, (int(midX), int(midY)), 8, (0, 0, 255), cv.FILLED)  # Mid point

    return volume


camW = 640
camH = 480
cap = cv.VideoCapture(0)
# set the dimensions of live video
cap.set(3, camW)
cap.set(4, camH)

barLength = camH / 2
volume = 30

detector = HandTrackingModule.handDetector()
posList = []
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    posList = detector.findPosition(img,draw=False)
    if len(posList) != 0:
       cv.circle(img, (posList[4][1], posList[4][2]), 10, (255, 0, 255), cv.FILLED)
       cv.circle(img, (posList[8][1], posList[8][2]), 10, (255, 0, 255), cv.FILLED)
       cv.line(img, (posList[4][1], posList[4][2]), (posList[8][1], posList[8][2]), (255, 255, 255), 3)
       midX = (posList[4][1] + posList[8][1]) / 2
       midY = (posList[4][2] + posList[8][2]) / 2
       cv.circle(img, (int(midX), int(midY)), 8, (0, 0, 255), cv.FILLED) # Mid point
       volume = volumeChange((posList[4][1], posList[4][2]), (posList[8][1], posList[8][2]), (int(midX), int(midY)))

    cv.rectangle(img, (30, 100), (70, 380), (130, 100, 100), 3)
    ratio = int(380 - 280 * volume / 100)
    cv.rectangle(img, (30, ratio), (70, 380), (130, 100, 100), cv.FILLED)
    cv.putText(img, str(volume) + "%", (20,90), cv.FONT_HERSHEY_COMPLEX, 1, (200, 130, 0), 3)
    cv.imshow("img", img)
    cv.waitKey(1)
