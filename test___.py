import cv2
import numpy as np
import imutils

def getContours(img, cThr=None, minArea=7000):
    if cThr is None:
        cThr = [100, 100]
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((3, 3))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(imgThre,
                                           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:

            # print(area)
            M = cv2.moments(i)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            cv2.drawContours(image, [i], -1, (0, 255, 0), 2)
            # cv2.drawContours(image, [contours[-1]], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 4, (255, 255, 255), -1)

            # find radius contours
            (x, y), radius = cv2.minEnclosingCircle(i)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(image, center, radius, (0, 0, 255), 2)
            cv2.circle(image, center, radius - 15, (0, 0, 255), 2)
            # Using cv2.putText() method
            cv2.putText(image, 'R = {}'.format(radius), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
            print('Ban kinh: {}'.format((radius)*2/100), 'mm')

            print('Ban kinh: {}'.format((radius - 15)*2/100), 'mm')
            # cv2.imshow('Canny Edges After Contouring', imgCanny)
            cv2.imshow('Contours', image)
            cv2.imwrite('result.jpg', image)
            return radius


if __name__ == '__main__':
    image = cv2.imread('data/2.jpg')
    getContours(image)


    # print(radius)
    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
