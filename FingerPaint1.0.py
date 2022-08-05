import cv2 as cv
import HandTrackingModule
import os
import math

# About the draw and erase part, creating a class requires a lot of work, use line on canvas will be a better option
# as how the teacher does in the video.

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
        print("Enter")
        if 0 < x < 80:
            No = 0
        elif 90 < x < 200:
            No = 1
        elif 210 < x < 350:
            No = 2
        elif 360 < x < 490:
            print("return 3")
            No = 3
        elif 500 < x < 635:
            No = 4

    return No


class Picture():
    red = []
    orange = []
    yellow = []
    green = []
    blue = []

    def __init__(self):
        pass

    def record(self, x, y, colorNo):
        if colorNo == 0:
            print("record")
            print((x,y))
            self.red.append((x, y))
            print(self.red[0])  # Value was changed after being appended to the red and i have no idea...
        elif colorNo == 1:
            self.orange.append([x, y])
        elif colorNo == 2:
            self.yellow.append([x, y])
        elif colorNo == 3:
            self.green.append([x, y])
        elif colorNo == 4:
            self.blue.append([x, y])

    def paint(self):

        if len(self.red) > 2:
            print((self.red[0]))
            i = 0
            for i in range(len(self.red) - 1):
                print("in")
                print((self.red[i]))
                breakpoint()
                cv.line(img, self.red[i], self.red[i + 1], color[0], 15)  #15 is thickness
        # if len(self.red) != 0:
        #     for position in self.red:
        #         cv.circle(img, position, 5, color[0], cv.FILLED)
        if len(self.orange) != 0:
            for position in self.orange:
                cv.circle(img, position, 5, color[1], cv.FILLED)
        if len(self.yellow) != 0:
            for position in self.yellow:
                cv.circle(img, position, 5, color[2], cv.FILLED)
        if len(self.green) != 0:
            for position in self.green:
                cv.circle(img, position, 5, color[3], cv.FILLED)
        # if len(self.blue) != 0:
        #     for position in self.blue:
        #       cv.circle(img, position, 5, color[4], cv.FILLED)

    def erase(self, x, y, radius2):
        if len(self.red) != 0:
            for position in self.red:
                dis = math.hypot(position[0] - x, position[1] - y)
                if dis <= radius2:
                    self.red.remove(position)
        if len(self.orange) != 0:
            for position in self.orange:
                dis = math.hypot(position[0] - x, position[1] - y)
                if dis <= radius2:
                    self.orange.remove(position)
        if len(self.yellow) != 0:
            for position in self.yellow:
                dis = math.hypot(position[0] - x, position[1] - y)
                if dis <= radius2:
                    self.yellow.remove(position)
        if len(self.green) != 0:
            for position in self.green:
                dis = math.hypot(position[0] - x, position[1] - y)
                if dis <= radius2:
                    self.green.remove(position)



# RBG color blue is a eraser
color = [[255, 0, 0], [27, 161, 226], [255, 255, 0], [0, 138, 0], [255, 255, 255], [255, 0, 255]]
colorPos = [[50, 185], [180, 185], [320, 185], [450, 185], [600, 185]]  # Point marked under the pigment
colorNo = 5  # Default color
picture = Picture()
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
        print(distance)
        # 3.Check the mode
        if distance < 50:  # The distance between index and middle fingers
            paintMode = False
            print("Selection mode")
            colorNo = chooseColor(x2, y2, colorNo)
            cv.rectangle(img, [x1 - 20, y1 - 30], [x2 + 20, y2 + 20], color[colorNo], cv.FILLED)
        else:
            paintMode = True
            print("Paint mode")
            if colorNo == 4:
                cv.circle(img, (x1, y1), 30, color[colorNo], cv.FILLED)
                picture.erase(x1, y1, 30 + 10)  # The distance between two centers
            else:
                cv.circle(img, (x1, y1), 10, color[colorNo], cv.FILLED)
            picture.record(x1, y1, colorNo)
    picture.paint()
    print("after")

    # 4.Mark a point for the chosen color
    if colorNo != 5:
        cv.circle(img, (colorPos[colorNo]), 10, color[colorNo], cv.FILLED)
    # Setting the header image
    img[0:170, 0:680] = header
    cv.imshow("Image", img)
    cv.waitKey(1)
