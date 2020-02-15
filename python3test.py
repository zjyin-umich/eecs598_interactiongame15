import cv2 as cv
import numpy as np
import sys
import random as rng


class ProcessImage:

    def DetectObject(self):

        vid = cv.VideoCapture(0)

        if (vid.isOpened() == False):
            print('Cannot open input video')
            return

        width = int(vid.get(3))
        height = int(vid.get(4))

        while (vid.isOpened()):
            rc, frame = vid.read()

            if (rc == True):

                # [pinkyX, pinkyY] = self.DetectBall(frame, 0, 154, 83, 19, 239, 115)
                self.DetectBall(frame, 0, 135, 196, 8, 255, 244)

                if (cv.waitKey(300) & 0xFF == ord('q')):
                    break

            else:
                break

        vid.release()
        cv.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectBall(self, frame, loH, loS, loV, hiH, hiS, hiV):

        lower = np.array([loH, loS, loV], dtype="uint8")
        upper = np.array([hiH, hiS, hiV], dtype="uint8")
        frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frame_HSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.dilate(mask, kernel)

        contour_image = np.copy(mask)
        contours, _ = cv.findContours(contour_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # greenMask = cv.inRange(frame_HSV,(loH, loS, loV),(hiH, hiS, hiV)) #This is the line being tested
        # output = cv.bitwise_and(frame,frame, mask= mask)

        # contours,  = cv.findContours(canny_output,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        contours_poly = []
        centers = []
        radius = []

        for i, c in enumerate(contours):
            # calculate moments for each contour
            # contours_poly[i] = cv.approxPolyDP(c, 3, True)
            if cv.contourArea(c) > 500:
                center, rad = cv.minEnclosingCircle(c)
                centers.append(center)
                radius.append(rad)

        drawing = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

        for i in range(len(centers)):
            # color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            # cv.drawContours(drawing, contours_poly, i, color)
            # cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
            #  (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
            cv.circle(frame, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), [0, 0, 255], -1)
            cv.putText(frame, "x: {}, y: {}".format(int(centers[i][0]), int(centers[i][1]), int(radius[i])),
                       (int(centers[i][0] + radius[i] + 10), int(centers[i][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       [0, 0, 255])
            cv.putText(frame, "{}".format(int(radius[i])),
                       (int(centers[i][0] + radius[i] + 10), int(centers[i][1] + 20)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       [0, 0, 255])

        cv.imshow('Contours', frame)


# Main Function
def main():
    processImg = ProcessImage()
    processImg.DetectObject()


if __name__ == "__main__":
    main()
