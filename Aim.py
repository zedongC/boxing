from random import randrange
import cv2 as cv
import math


# We do not create new object, we just renew the object by generate()
class Target:

    def __init__(self):
        self.targetTime = 0
        self.hitEffectTime = 21
        self.hit = False
        # Choose a hit effect randomly
        if randrange(0, 2) == 0:
            self.effectImg = cv.imread("source/effect2.png")
        else:
            self.effectImg = cv.imread("source/effect1.png")

    # Given face rectangle coordinates
    def generate(self, top, bot):
        if randrange(0, 2) == 0:
            self.side = "left"
            self.centerX = randrange(top[0], int((bot[0] + top[0]) / 2))  # Targets will be generated on the left side
            self.effectImg = cv.imread("source/effect2.png")  # Choose a hit effect randomly
        else:
            self.side = "right"
            self.centerX = randrange(int((bot[0] + top[0]) / 2), bot[0])
            self.effectImg = cv.imread("source/effect1.png")


        self.centerY = randrange(top[1], bot[1])
        self.hitEffectTime = 21
        self.targetTime = 0  # Restart


    def draw(self, img):
        x, y = self.centerX, self.centerY
        cv.line(img, (x, y - 35 - 15), (x, y - 15), (0, 255, 0), 4)
        cv.line(img, (x - 35 - 15, y), (x - 15, y), (0, 255, 0), 4)
        cv.line(img, (x + 15, y), (x + 35 + 15, y), (0, 255, 0), 4)
        cv.line(img, (x, y + 15), (x, y + 35 + 15), (0, 255, 0), 4)
        cv.circle(img, (x, y), 35, (0, 255, 0), 6)
        cv.circle(img, (x, y), 22, (0, 255, 0), 3)
        # if self.side == "left":
        #     cv.putText(img, "left", (self.centerX, self.centerY - 50), cv.FONT_HERSHEY_PLAIN, 5, (80, 100, 255), 5)
        # else:
        #     cv.putText(img, "right", (self.centerX, self.centerY - 50), cv.FONT_HERSHEY_PLAIN, 5, (80, 100, 255), 5)
        self.targetTime += 1

    def hitEffect(self, img, canvas):
        x, y = self.centerX, self.centerY

        # Put hit effect image in canvas (y first and x second, it is a little weird
        canvas[y - 72:y + 72, x - 81:x + 81] = self.effectImg
        if self.side == "left":
            cv.putText(img, self.result, (self.centerX - 400, self.centerY), cv.FONT_HERSHEY_PLAIN, 4, (80, 100, 255), 5)
        else:
            cv.putText(img, self.result, (self.centerX + 100, self.centerY), cv.FONT_HERSHEY_PLAIN, 4, (80, 100, 255), 5)
        self.hitEffectTime += 1

    def missEffect(self, img):
        x, y = self.centerX, self.centerY
        cv.line(img, (x, y - 35 - 15), (x, y - 15), (0, 0, 255), 4)
        cv.line(img, (x - 35 - 15, y), (x - 15, y), (0, 0, 255), 4)
        cv.line(img, (x + 15, y), (x + 35 + 15, y), (0, 0, 255), 4)
        cv.line(img, (x, y + 15), (x, y + 35 + 15), (0, 0, 255), 4)
        cv.circle(img, (x, y), 40, (0, 0, 255), 6)
        cv.circle(img, (x, y), 25, (0, 0, 255), 3)

        cv.putText(img, "MISS", (self.centerX + 100, self.centerY), cv.FONT_HERSHEY_PLAIN, 3,
                   (80, 100, 255), 5)
        self.targetTime += 1


    def hitOrMiss(self,fist1, fist2, canvas, opponentHP):
        distance1 = math.sqrt((fist1[0] - self.centerX) ** 2 + (fist1[1] - self.centerY) ** 2)
        distance2 = math.sqrt((fist2[0] - self.centerX) ** 2 + (fist2[1] - self.centerY) ** 2)
        print(distance2, distance1)


        x, y = self.centerX, self.centerY
        if distance1 <= 35 or distance2 <= 35:
            self.result = "PERFECT!"
            self.hit = True
            # Put hit effect image in canvas (y first and x second, it is a little weird
            canvas[y - 72:y + 72, x - 81:x + 81] = self.effectImg
            self.hitEffectTime = 0
            opponentHP -= 10
            # cv.imshow("a", canvas)
        else:
            self.result = "MISS"
        return opponentHP
        # miss and perfect damaging blow