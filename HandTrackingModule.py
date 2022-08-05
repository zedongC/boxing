import cv2 as cv
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict


# That's a data class
class handDetector:

    def __init__(self, mode=False, maxHands=2, complexity = 1, detectionCon=0.5, trackCon=0.5):  # con - confidence
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.myHands = mp.solutions.hands
        self.hands = self.myHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.myHands.HAND_CONNECTIONS)  # draw the hand joints and the lines
        return img

    def handsNumber(self):
        num = 0
        if self.results.multi_hand_landmarks == None:
            num = 0
        else:
            if len(self.results.multi_hand_landmarks) == 1:
                num = 1
            elif len(self.results.multi_hand_landmarks) == 2:
                num = 2
        return num

    def label(self, handNo):
        # Enumerate the list and convert the Protobuf message to a Python dict
        for idx, hand_handedness in enumerate(self.results.multi_handedness):
            handedness_dict = MessageToDict(hand_handedness)
            print(handedness_dict['classification'][0]['label'])

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []
        # left = []
        # right = []
        # lmList.append(left)
        # lmList.append(right)
        # for handNo in range(1):  # Record the first hand and then the second one
        #         # print(self.results.multi_hand_landmarks)
        #
        #         myHand = self.results.multi_hand_landmarks[handNo]
        #         # breakpoint()
        #         for id, lm in enumerate(myHand.landmark): # id is the id of each landmark(joints)
        #             h, w, c = img.shape
        #
        #             # find out the position of each landmark in the image,
        #             # given the ratio of those position in the picture
        #             cx, cy = int(lm.x * w), int(lm.y * h)
        #             lmList[handNo].append([id, cx, cy])
        #             if draw:
        #                 cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)


        ############################################################################################
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark): # id is the id of each landmark(joints)
                h, w, c = img.shape

                # find out the position of each landmark in the image,
                # given the ratio of those position in the picture
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        return lmList



def main():
    pTime = 0
    cTime = 0

    cap = cv.VideoCapture(0)
    # set the dimensions of live video
    cap.set(3, 640)
    cap.set(4, 480)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img) #Get the model hands on the image

        lmList = detector.findPosition(img) #Collect all the positions
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.imshow("img", img)
        cv.waitKey(1)


# _name_ is a implicit variable whose value is set as __main__.
# If other files import this module, they will execute this main function first and then execute other codes
if __name__ == '__main__':
    main()
