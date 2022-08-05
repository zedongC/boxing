import cv2 as cv
import mediapipe as mp


class poseDetector():
    def __init__(self, static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):  # con - confidence

        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def findPose(self, img, draw = True):

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
           self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw = True):
        lmList = []

        if self.results.pose_landmarks:

            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # find out the position of each landmark in the image,
                # given the ratio of those position in the picture
                # z is the depth, make it a positive integer, so it can be
                # compared more easily.
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(-lm.z * 100)
                lmList.append([id, cx, cy, cz])
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
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img) #Get the model hands on the image

        lmList = detector.findPosition(img) #Collect all the positions
        if len(lmList) != 0:
            print(lmList[4])


        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.imshow("img", img)
        cv.waitKey(1)


# _name_ is a implicit variable whose value is set as __main__.
# If other files import this module, they will execute this main function first and then execute other codes
if __name__ == '__main__':
    main()
