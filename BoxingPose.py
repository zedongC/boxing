import cv2 as cv
import math
import PosTrack
import Aim
import EnemyFist
import numpy as np
from random import randrange

# 1. Too big punch and no comment wait first, then generate,
# so we get more accurate position. Set a detecting system to ensure
# that the player is in the right area. If she/he is not, show it
camW = 1280
camH = 720
cap = cv.VideoCapture(0)
# set the dimensions of live video
cap.set(3, camW)
cap.set(4, camH)

barLength = camH / 2
volume = 30
finalInterval = 2  # Easy: 10 Medium: 6 Hard: 2
detector = PosTrack.poseDetector()
target = Aim.Target()
attack = EnemyFist.fist()
# To generate the first one
target.targetTime = 30
attack.warningTime = 30
posList = []
intervalTimer = 0
mode = 0  # 0 is ducking and 1 is punching time
playerHP = 100
opponentHP = 100
opponentWin = False
playerWin = False

def nextMode():
    if randrange(0, 2) == 0:
        # Do not actually change the outer mode?? yes, you need to return it,
        # considering the scope of the mode
        rnd = 0
    else:
        rnd = 1
    return rnd  # Seems it does not work, make a class for mode maybe...wait, it might be working now

def combineImage(img, canvas):
    # Combine the imgCanvas and img
    imgGray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, canvas)

    return img

def result(result):
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)

        cv.putText(img, result, (370, 310), cv.FONT_HERSHEY_TRIPLEX, 4, (200, 130, 0), 5)
        cv.imshow("img", img)
        cv.waitKey(1)


while not(opponentWin) and not(playerWin):
    targetCanvas = np.zeros((720, 1280, 3), np.uint8)
    enemyCanvas = np.zeros((720, 1280, 3), np.uint8)
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.findPose(img)
    posList = detector.findPosition(img, draw=False)
    if len(posList) != 0:

        # Right
        x1, y1 = posList[13][1], posList[13][2]  # Elbow
        x2, y2 = posList[11][1], posList[11][2]  # Shoulder
        distanceR = math.sqrt((x1 - x2) **2 + (y1 - y2) ** 2)

        # left
        x3, y3 = posList[14][1], posList[14][2]  # Elbow
        x4, y4 = posList[12][1], posList[12][2]  # Shoulder
        distanceL = math.sqrt((x3 - x4) ** 2 + (y3 - y4) ** 2)

        mx1, my1 = posList[10][1], posList[10][2]  # Left mouth
        mx2, my2 = posList[9][1], posList[9][2]  # Right mouth
        noseX, noseY = posList[0][1], posList[0][2]  # Nose
        # cv.rectangle(img, (mx1 - 25, my1 - 50), (mx2 + 15, my2 + 30), (0, 255, 255), 4)

        #############################Enemy Attack################################
        if intervalTimer == 1 and mode == 0:
            attack.generate(noseX, noseY)
        if intervalTimer < 1 and mode == 0:
            if attack.hitEffectTime > 5:
                if attack.warningTime < 18:  # Easy: 22 Medium: 18 Hard: 16
                    attack.punchWarning(enemyCanvas)
                    # Wait several seconds and decide hit or miss
                    if attack.warningTime > 15:  # Easy: 19 Medium: 15 Hard: 13
                        playerHP = attack.hitOrMiss(noseX, noseY, enemyCanvas, img, playerHP)
                else:
                    intervalTimer = finalInterval
                    mode = nextMode()
            else:
                # When hitOrMiss method decides the target is hit, it will reset the hitTime
                # and this else branch will execute
                attack.hitEffect(img, targetCanvas)
                if attack.hitEffectTime > 5:
                    intervalTimer = finalInterval
                    mode = nextMode()
        img = combineImage(img, enemyCanvas)

        #############################Target#########################################
        # Wait until the last second of the interval, generate the new
        # target so the coordinates will be more accurate
        if intervalTimer == 1 and mode == 1:
            target.generate([mx1 - 25, my1 - 50], [mx2 + 15, my2 + 30])
        if intervalTimer < 1 and mode == 1:
            # hitTime: the time that the hit effect is shown. The effect will last 5 rounds
            # targetTime: the time that the target is shown. The same target will show 26 rounds
            if target.hitEffectTime > 5:
                if target.targetTime < 25:  # Easy: 27 Medium: 25 Hard: 23
                    if target.targetTime < 20:  # Easy: 22 Medium: 20 Hard: 18
                        target.draw(img)
                        if distanceR < 80:  # That means the fighter does strike
                            # Check both index and pinky fingers
                            opponentHP = target.hitOrMiss([posList[19][1], posList[19][2]], [posList[17][1], posList[17][2]], targetCanvas, opponentHP)
                        elif distanceL < 80:
                            opponentHP = target.hitOrMiss([posList[20][1], posList[20][2]], [posList[18][1], posList[18][2]], targetCanvas, opponentHP)
                    else:
                        target.missEffect(img)
                else:
                    intervalTimer = finalInterval
                    mode = nextMode()
            else:
                # When hitOrMiss method decides the target is hit, it will reset the hitTime
                # and this else branch will execute
                target.hitEffect(img, targetCanvas)
                if target.hitEffectTime > 5:
                    intervalTimer = finalInterval
                    mode = nextMode()
        img = combineImage(img, targetCanvas)

        #####################Health points########################
        # Player
        cv.rectangle(img, (50, 130), (100, 580), (0, 0, 0), 3)
        ratio = int(533 - 400 * playerHP / 100)
        cv.rectangle(img, (53, ratio), (97, 577), (0, 0, 255), cv.FILLED)
        cv.putText(img, "PLAYER", (30, 110), cv.FONT_HERSHEY_COMPLEX, 1, (200, 130, 0), 3)
        if playerHP < 20:
            opponentWin = True

        # Enemy
        cv.rectangle(img, (1140, 130), (1190, 580), (0, 0, 0), 3)
        ratio = int(533 - 400 * opponentHP / 100)
        cv.rectangle(img, (1143, ratio), (1187, 577), (0, 0, 255), cv.FILLED)
        cv.putText(img, "OPPONENT", (1070, 110), cv.FONT_HERSHEY_COMPLEX, 1, (200, 130, 0), 3)
        if opponentHP < 20:
            playerWin = True

    intervalTimer -= 1  # Counting down
    cv.imshow("img", img)
    cv.waitKey(1)

if playerWin:
    result("WINNING!!!")
else:
    result("DEFEAT")





