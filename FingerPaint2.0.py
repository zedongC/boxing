import cv2 as cv
import HandTrackingModule
import os
import math
import numpy as np

# In the video, the teacher uses the combination of two image to avoid restoring a large number of positions.
# Since the img is renewed continuously, if we use one image, we need to paint all the position by loop every time when
# img is renewed, which is troublesome and cumbersome. But imgCanvas will not be renewed so it will keep all the picture

folderPath = "PaintColors"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    w = int(image.shape[1] * 5)
    h = int(image.shape[0] * 5)
    dimensions = (w, h)
    image = cv.resize(image, dimensions, interpolation=cv.INTER_AREA)
    overlayList.append(image)
print(len(overlayList))

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandTrackingModule.handDetector(detectionCon=0.85)

# keep the color point so the user knows what color she is using
def chooseColor(x, y, colorNo):
    No = colorNo
    if y < 160:
        if 0 < x < 80:
            No = 0
        elif 90 < x < 200:
            No = 1
        elif 210 < x < 350:
            No = 2
        elif 360 < x < 490:
            No = 3
        elif 500 < x < 635:
            No = 4
    return No


# RBG color blue is a eraser
color = [[255, 0, 0], [27, 161, 226], [255, 255, 0], [0, 138, 0], [255, 255, 255], [84, 84, 84]]
colorPos = [[50, 185], [180, 185], [320, 185], [450, 185], [600, 185]]  # Point marked under the pigment
colorNo = 5  # Default color
xStart, yStart = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
cv.imshow("can", imgCanvas)

while True:
    header = overlayList[0]
    # 1.Import images
    success, img = cap.read()
    img = cv.flip(img, 1)

    # 2.Find the hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip for the index finger
        x1, y1 = lmList[8][1:]
        # Tip for the middle finger
        x2, y2 = lmList[12][1:]

        distance = math.hypot(x2 - x1, y2 - y1)
        # 3.Check the mode
        if distance < 50:  # The distance between index and middle fingers
            # print("Selection mode")
            colorNo = chooseColor(x2, y2, colorNo)
            cv.rectangle(img, [x1 - 20, y1 - 30], [x2 + 20, y2 + 20], color[colorNo], cv.FILLED)
        else:
            # print("Paint mode")
            if colorNo == 4:  # Erase
                cv.circle(imgCanvas, (x1, y1), 30, (0, 0, 0), cv.FILLED)  # The canvas is painted(erased) black
                cv.circle(img, (x1, y1), 30, color[colorNo], cv.FILLED)  # Show the eraser
            elif colorNo == 5:  # Default
                cv.circle(img, (x1, y1), 12, color[colorNo], cv.FILLED)
            else:
                if xStart != 0 and yStart != 0:
                    cv.line(imgCanvas, (xStart, yStart), (x1, y1), color[colorNo], 12)
        xStart, yStart = x1, y1

    # 4.Mark a point for the chosen color
    if colorNo != 5:
        cv.circle(img, (colorPos[colorNo]), 10, color[colorNo], cv.FILLED)
    # Setting the header image
    img[0:170, 0:680] = header

    # Combine the imgCanvas and img
    imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, imgCanvas)
    # img = cv.addWeighted(img, 0.5, imgCanvas, 0.5, 0) dim version

    cv.imshow("Image", img)
    # cv.imshow("Canvas", imgCanvas)
    cv.waitKey(1)
