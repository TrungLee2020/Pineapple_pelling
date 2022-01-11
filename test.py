from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

class obj_size():

    def __init__(self, image_path, width):
        self.image_path = image_path
        self.width = width

    # Define midpoint coordinate operation
    def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


    def compute(self):
        # load image, convert grayscale, blur
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # Binary image
        # ret, thresh = cv2.threshold(edged.copy(), 150, 200, 0)
        # Calculate the coordinates of the four corner points of the black square
        cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        # sort the contours from left-to-right and initialize the
        # 'pixels per metric' calibration variable
        (cnts, _) = contours.sort_contours(cnts)
        pixelsPerMetric = None

        # define a list for keeping length or each object
        mylist = []
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area > 500:
                print(area)
                # compute the rotated bounding box ò the contour
                orig = image.copy()
                box = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")

                box = perspective.order_points(box)
                cv2.drawContours(orig, [box.astype("int")], -1, (0,255,0), 2)

                for (x, y) in box:
                    cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

                (tl, tr, br, bl) = box
                (tltrX, tltrY) = self.midpoint(tl, tr)
                (blbrX, blbrY) = self.midpoint(bl, br)

                # compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-righ and bottom-right
                (tlblX, tlblY) = self.midpoint(tl, bl)
                (trbrX, trbrY) = self.midpoint(tr, br)

                # draw the midpoints on the image
                cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

                # draw lines between the midpoints
                ###cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                ###	(255, 0, 255), 2)
                ###cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                ###	(255, 0, 255), 2)

                cv2.line(orig, (int(tr[0]), int(tr[1])), (int(bl[0]), int(bl[1])),
                         (255, 0, 255), 2)
                cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                         (255, 0, 255), 2)

                # compute the Euclidean distance between the midpoints
                ###dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                ###dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                dA = dist.euclidean((tr[0], tr[1]), (bl[0], bl[1]))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                # if the pixels per metric has not been initialized, then
                # compute it as the ratio of pixels to supplied metric
                # (in this case, inches)
                if pixelsPerMetric is None:
                    pixelsPerMetric = dB / self.width

                # compute the size of the object
                dimA = dA / pixelsPerMetric
                dimB = dB / pixelsPerMetric

                # keep dimB value in a list
                mylist.append(dimA)
                ##print (mylist[-1])

                # draw the object sizes on the image
                ##cv2.putText(orig, "{:.1f}in".format(dimA),
                ##	(int(tr[0] - 15), int(tr[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                ##	0.65, (255, 255, 255), 2)
                ##cv2.putText(orig, "{:.1f}in".format(dimB),
                ##	(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                ##	0.65, (255, 255, 255), 2)

                # show the output image
                ##cv2.imshow("Image", orig)
                ##cv2.waitKey(0)
                ##cv2.waitKey(0)
                ##cv2.waitKey(0)
                ##cv2.waitKey(0)

                # print all dimB in a list
            return str(mylist[-1])

