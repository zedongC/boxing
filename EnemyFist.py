from random import randrange
import cv2 as cv
import math

class fist:

    def __init__(self):
        self.warningTime = 0
        self.hitEffectTime = 21
        self.hit = False

    # x and y are nose's coordinates
    def generate(self, x, y):

        self.centerX = randrange(x - 5, x + 5)
        self.centerY = randrange(y - 5, y + 5)

        self.warningTime = 0  # Restart

    def punchWarning(self, canvas):
        x, y = self.centerX, self.centerY
        # Sometimes the coordinates might be out of range if the player does not
        # stand on the right area
        canvas[y - 30:y + 30, x - 34:x + 34] = cv.imread("source/warning.jpg")
        self.warningTime += 1

    def realPunch(self, canvas):
        x, y = self.centerX, self.centerY
        canvas[y - 38:y + 38, x - 43:x + 43] = cv.imread("source/realPunch.jpg")


    def hitEffect(self, img, canvas):
        x, y = self.centerX, self.centerY

        # Put hit effect image in canvas (y first and x second, it is a little weird
        canvas[y - 72:y + 72, x - 81:x + 81] = cv.imread("source/effect1.png")
        cv.putText(img, self.result, (self.centerX - 200, self.centerY), cv.FONT_HERSHEY_PLAIN, 3, (80, 100, 255), 5)
        self.hitEffectTime += 1


    # Wait several seconds and then decide hit or miss
    # x and y are the current coordinates of the center of the face
    def hitOrMiss(self, x, y, canvas, img, playerHP):
        distance = math.sqrt((x - self.centerX) ** 2 + (y - self.centerY) ** 2)
        # Between punchWarning 38 and 43
        if distance <= 55:
            self.result = "HIT"
            self.hit = True
            # Put hit effect image in canvas (y first and x second, it is a little weird
            print("y", self.centerY)
            canvas[self.centerY - 72:self.centerY + 72, self.centerX - 81:self.centerX + 81] = cv.imread("source/effect1.png")
            self.hitEffectTime = 0
            playerHP -= 10
            # cv.imshow("a", canvas)
        else:
            # self.result = "AWESOME!"
            self.realPunch(canvas)
            cv.putText(img, "AWESOME!", (self.centerX - 400, self.centerY), cv.FONT_HERSHEY_PLAIN, 4,
                       (80, 100, 255), 5)
        return playerHP
        # miss and perfect damaging blow