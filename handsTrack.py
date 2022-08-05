import cv2
import cv2 as cv
import mediapipe as mp
import time


cap = cv.VideoCapture(0)
# set the dimensions of live video
cap.set(3, 640)
cap.set(4, 480)

myHands = mp.solutions.hands
hands = myHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark): # id is the id of each landmark(joints)
                h, w, c = img.shape
                # find out the position of each landmark in the image,
                # given the ratio of those position in the picture
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 0:
                    cv.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, myHands.HAND_CONNECTIONS) # draw the hand joints and the lines
    cv.imshow("img", img)
    cv.waitKey(1)
