import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
# set the dimensions of live video
cap.set(3, 6400)
cap.set(4, 4800)

def empty(a):
    pass


cv.namedWindow("TrackBars")
cv.resizeWindow("TrackBars", 640, 240)
cv.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv.createTrackbar("Sat Max", "TrackBars", 34, 255, empty)
cv.createTrackbar("Val Min", "TrackBars", 140, 255, empty)
cv.createTrackbar("Val Max", "TrackBars", 211, 255, empty)

def getContours(canny):
    contours,hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        peri = cv.arcLength(cnt, True)
        # we're instructing OpenCV to calculate an approximated polygon whose perimeter can only
        # differ from the original contour by an epsilon ratio – specifically, 2% of the original arc length
        approx = cv.approxPolyDP(cnt, 0.02 * peri, True) # lists of positions
        cornerNum = len(approx)
        # print(cornerNum)

        # filter contours a rectangle bigger than 100
        if area > 5000 :
           cv.drawContours(img, cnt, -1, (255, 0, 0), 3)  # draw the contour on the img which is the original image
           x, y, w, h = cv.boundingRect(approx)  # get x,y and width and height
           print(area)

    return approx
points = []
while True:
    success, img = cap.read()
    imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(imgHSV, (5,5),cv.BORDER_DEFAULT)

    hMin = cv.getTrackbarPos("Hue Min", "TrackBars")
    hMax = cv.getTrackbarPos("Hue Max", "TrackBars")
    sMin = cv.getTrackbarPos("Sat Min", "TrackBars")
    sMax = cv.getTrackbarPos("Sat Max", "TrackBars")
    vMin = cv.getTrackbarPos("Val Min", "TrackBars")
    vMax = cv.getTrackbarPos("Val Max", "TrackBars")
    mask1 = cv.inRange(imgHSV, np.array([hMin, sMin, vMin]), np.array([hMax, sMax, vMax]))
    # mask1 = cv.inRange(blur, np.array([hMin, sMin, vMin]), np.array([hMax, sMax, vMax]))
    canny = cv.Canny(mask1, 125, 175)
    kernel = np.ones((5,5))
    imgDial = cv.dilate(canny, kernel, iterations=2)
    imgThres = cv.erode(imgDial, kernel, iterations=1)

    points = getContours(imgThres)
    print(points)
    # for point in points:
    #     print(point)
    #     cv.circle(img, (point[0], point[1]), 10, (255, 0, 0), cv.FILLED)
    pts1 = np.float32([[]])
    cv.imshow("img", img)
    # findColor(img, color)
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break