import cv2 as cv
import HandTrackingModule2  # Copy from cvzone and add complexity in init
from time import sleep

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandTrackingModule2.HandDetector(detectionCon=0.8,minTrackCon=0.1, maxHands=2)

class Hand:
    def __init__(self, lmList, handType):
        self.lmList = lmList
        self.handType = handType

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    # 2.Find the hand landmarks
    hands, img = detector.findHands(img, flipType=False)


    # If the camera only detects one hand
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 landmarks points
        centerPoint1 = hand1["center"]  # Center of the hand cx, cy
        handType1 = hand1["type"]  # Hand Type Left or Right
        # x1, y1 = lmList1[0][5][1], lmList1[0][5][2]
        # x2, y2 = lmList1[0][17][1], lmList1[0][17][2]
        # print(lmList1[17][0])
        # If it detects two
        # if handType1 == "left":
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 landmarks points
            centerPoint2 = hand2["center"]  # Center of the hand cx, cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            if handType2 == "left":
                x1_left, y1_left = lmList2[5][0], lmList2[5][1]  # Left
                x2_left, y2_left = lmList2[17][0], lmList2[17][1]  # Left
                x1, y1 = lmList1[5][0], lmList1[5][1]  # Right
                x2, y2 = lmList1[17][0], lmList1[17][1]  # Right
                rightDis = detector.findDistance((x1, y1), (x2, y2))
                leftDis = detector.findDistance((x1_left, y1_left), (x2_left, y2_left))
            else:
                x1_left, y1_left = lmList1[5][0], lmList1[5][1]  # Right
                x2_left, y2_left = lmList1[17][0], lmList1[17][1]  # Right
                x1, y1 = lmList2[5][0], lmList2[5][1]  # Left
                x2, y2 = lmList2[17][0], lmList2[17][1]  # Left
                leftDis = detector.findDistance((x1, y1), (x2, y2))
                rightDis = detector.findDistance((x1_left, y1_left), (x2_left, y2_left))
            # print(rightDis, "right")
            # print(leftDis, "left")
            if rightDis[0] > 150 or leftDis[0] > 150:
                print("hit")
                sleep(0.15)
            # bind the left and right two respective class
            # x1_left, y1_left = lmList[1][5][1], lmList[1][5][2]
            # x2_left, y2_left = lmList[1][17][1], lmList[1][17][2]


    cv.imshow("img", img)
    cv.waitKey(1)