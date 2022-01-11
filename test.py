import cv2
import numpy as np
from scipy.spatial import distance as dist


# Define midpoint coordinate operation
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def measure(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Binary image
    ret, thresh = cv2.threshold(gray, 150, 200, 0)
    # Calculate the coordinates of the four corner points of the black square
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            print(area)

            # Find the geometric distance of the outline
            M = cv2.moments(cnt)
            # Get the bounding rectangle of the outline, x, y is the coordinate point of the upper left corner of the
            # green frame, w, h is the length and width of the green frame
            x, y, w, h = cv2.boundingRect(cnt)
            # Calculate the minimum outline, red frame
            rect = cv2.minAreaRect(cnt)
            # Calculate the image coordinates of the four corners of the red frame
            box = cv2.boxPoints(rect)
            #  is an integer, so the coordinates are converted to integer
            box = np.int0(box)

            if M['m00'] != 0:
                # print(M)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                # Based on the center point obtained by the geometric distance, draw the center circle, blocked by the
                # blue line, so you can't see it.
                cv2.circle(img, (np.int(cx), np.int(cy)), 2, (0, 255, 255), -1)

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                for (x, y) in box:
                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    # tl upper left corner image coordinate, tr upper right corner image coordinate,
                    # br lower right corner image coordinate, bl lower left corner image coordinate
                    (tl, tr, br, bl) = box
                    # Calculate the center point of the 4 sides of the red frame
                    (tltrX, tltrY) = midpoint(tl, tr)
                    (blbrX, blbrY) = midpoint(bl, br)
                    (tlblX, tlblY) = midpoint(tl, bl)
                    (trbrX, trbrY) = midpoint(tr, br)
                    #
                    cv2.circle(img, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                    cv2.circle(img, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                    cv2.circle(img, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                    cv2.circle(img, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
                    #  4 points, that is, 2 blue lines in the picture
                    cv2.line(img, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                             (255, 0, 0), 2)
                    cv2.line(img, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                             (255, 0, 0), 2)
                    # Calculate the coordinates of the center point
                    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                    # Convert the image length to the actual length, 6.5 is equivalent to the scale, I use the mm unit,
                    # that is, 1mm is equivalent to 6.5 images

                    dimA = dA / 6.5
                    dimB = dB / 6.5
                    # Print the calculation result on the original image, which is the yellow content.

                    cv2.putText(img, "{:.1f}mm".format(dimA),
                                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (0, 255, 255), 2)
                    cv2.putText(img, "{:.1f}mm".format(dimB),
                                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (0, 255, 255), 2)
        cv2.imshow("mo", img)


# Start the camera and set the resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# ret, frame = cap.read()
# img = cv2.flip(frame, -1)
img = cv2.imread('3.jpg')
# Create a GUI window in the form of adaptive
cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
# Contact the image and window by name
cv2.imshow("input image", img)
cv2.waitKey(0)
measure(img)
cv2.waitKey(0)

