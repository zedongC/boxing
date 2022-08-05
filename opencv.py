import cv2 as cv
import numpy as np




def empty(a):
    pass


cv.namedWindow("TrackBars")
cv.resizeWindow("TrackBars", 640, 240)
cv.createTrackbar("Hue Min", "TrackBars", 22, 179, empty)
cv.createTrackbar("Hue Max", "TrackBars", 30, 179, empty)
cv.createTrackbar("Sat Min", "TrackBars", 108, 255, empty)
cv.createTrackbar("Sat Max", "TrackBars", 255 , 255, empty)
cv.createTrackbar("Val Min", "TrackBars", 90, 255, empty)
cv.createTrackbar("Val Max", "TrackBars", 221, 255, empty)


cap = cv.VideoCapture(0)
# set the dimensions of live video
cap.set(3, 640)
cap.set(4, 480)

color = [[13, 69, 88, 19, 148, 171]]

def findColor(img, color):
    lower = np.array(color[0][0:3])
    upper = np.array(color[0][3:6])
    mask = cv.inRange(imgHSV, lower, upper)
    # cv.imshow("Mask", mask)
    # getContours(mask)

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
        if area > 500 :
         # cv.drawContours(img, cnt, -1, (255, 0, 0), 3)  # draw the contour on the img which is the original image
         x, y, w, h = cv.boundingRect(approx)  # get x,y and width and height
         print(area)

    return int(x + w / 2), int(y)

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
    mask1 = cv.inRange(blur, np.array([hMin, sMin, vMin]), np.array([hMax, sMax, vMax]))
    canny = cv.Canny(mask1, 125, 175)

    points.append(getContours(canny))
    for point in points:
        print(point)
        cv.circle(img, (point[0], point[1]), 10, (255, 0, 0), cv.FILLED)
    cv.imshow("img", img)
    findColor(img, color)
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break










    # result = cv.bitwise_and(img, img, mask = mask)
    # total = np.hstack((result, img))
    # cv.imshow("Video", imgHSV)
    # cv.imshow("Total", total)









# img = cv.imread("source/side.jpg")
# imgGray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#
 # imgRe = cv.resize(img,(900,900))
# imgCanny = cv.Canny(imgRe, 65, 45)
# imgHSV = cv.cvtColor(imgRe, cv2.COLOR_BGR2HSV)
# # cv.imshow("Image", imgGray)
# # cv.imshow("CANNY", imgCanny)
# print(img.shape)
# # cv.imshow("re", imgRe)
# cv.imshow("hsv", imgHSV)
# cv.waitKey(0)










