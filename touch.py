import cv2 as cv
import numpy as np
import sys
import random as rng

class ProcessImage:

    def DetectObject(self):

        vid = cv.VideoCapture(0)

        if(vid.isOpened() == False):
            print('Cannot open input video')
            return

        width = int(vid.get(3))
        height = int(vid.get(4))

        while(vid.isOpened()):
            rc, frame = vid.read()

            if(rc == True):
                    
                #[pinkyX, pinkyY] = self.DetectBall(frame, 0, 154, 83, 19, 239, 115)
                self.DetectBall(frame, 0, 154, 83, 19, 239, 115)

                
                
                #Pinky Actual
                #cv.circle(frame, (int(pinkyX), int(pinkyY)), 20, [0,0,255], 2, 8)
                #cv.line(frame,(int(pinkyX), int(pinkyY + 20)), (int(pinkyX + 50), int(pinkyY + 20)), [100,100,255], 2,8)
                #cv.putText(frame, "X = ", (int(pinkyX + 50), int(pinkyY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                #cv.putText(frame, str(pinkyX), (int(pinkyX + 65), int(pinkyY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                

                #cv.imshow('Input', frame)

                if (cv.waitKey(300) & 0xFF == ord('q')):
                    break

            else:
                break

        vid.release()
        cv.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectBall(self, frame, loH, loS, loV, hiH, hiS, hiV):

        lower = np.array([loH, loS, loV], dtype = "uint8")
        upper = np.array([hiH, hiS, hiV], dtype = "uint8")
        frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frame_HSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.dilate(mask, kernel)

        contour_image = np.copy(mask)
        contours, _ = cv.findContours(contour_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


        #greenMask = cv.inRange(frame_HSV,(loH, loS, loV),(hiH, hiS, hiV)) #This is the line being tested
        #output = cv.bitwise_and(frame,frame, mask= mask)


        #contours,  = cv.findContours(canny_output,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        contours_poly = []
        centers = []
        radius = []
        
        for i, c in enumerate(contours):
           # calculate moments for each contour
           #contours_poly[i] = cv.approxPolyDP(c, 3, True)
           if cv.contourArea(c)>500:
               center, rad = cv.minEnclosingCircle(c)
               centers.append(center)
               radius.append(rad)

        drawing = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

        for i in range(len(centers)):
            #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            #cv.drawContours(drawing, contours_poly, i, color)
            #cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
            #  (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
            cv.circle(frame, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), [0,0,255], -1)
            cv.putText(frame, "x: {}, y: {}".format(int(centers[i][0]), int(centers[i][1]), int(radius[i])), (int(centers[i][0] + radius[i] + 10), int(centers[i][1])), cv.FONT_HERSHEY_SIMPLEX,0.5, [0,0,255])
            cv.putText(frame, "{}".format(int(radius[i])), (int(centers[i][0] + radius[i] + 10), int(centers[i][1] + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [0,0,255])
    
    
        cv.imshow('Contours', frame)
           # display the image
           #cv.imshow("Image", img)

        
        
        # Dilate
        #kernel = np.ones((5, 5), np.uint8)
        #greenMaskDilated = cv.dilate(greenMask, kernel)

        # Find ball blob as it is the biggest green object in the frame
        #[nLabels, labels, stats, centroids] = cv.connectedComponentsWithStats(greenMaskDilated, 8, cv.CV_32S)

        # First biggest contour is image border always, Remove it
        #stats = np.delete(stats, (0), axis = 0)
        #try:
        #    maxBlobIdx_i, maxBlobIdx_j = np.unravel_index(stats.argmax(), stats.shape)

        # This is our ball coords that needs to be tracked
        #    ballX = stats[maxBlobIdx_i, 0] + (stats[maxBlobIdx_i, 2]/2)
        #    ballY = stats[maxBlobIdx_i, 1] + (stats[maxBlobIdx_i, 3]/2)
        #    return [ballX, ballY]
        #except:
        #       pass

        #return [0,0]
        
        
    


#Main Function
def main():

    processImg = ProcessImage()
    processImg.DetectObject()


if __name__ == "__main__":
    main()


