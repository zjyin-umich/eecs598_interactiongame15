import cv2 as cv

low_H = 0
low_S = 0
low_V = 0
high_H = 180
high_S = 255
high_V = 255


def low_H_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos('Low H', 'HSV Frame', low_H)

def high_H_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos('High H', 'HSV Frame', high_H)

def low_S_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos('Low S', 'HSV Frame', low_S)

def high_S_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos('High S', 'HSV Frame', high_S)

def low_V_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos('Low V', 'HSV Frame', low_V)

def high_V_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos('High V', 'HSV Frame', high_V)

cap = cv.VideoCapture(1)
cv.namedWindow('Captured Video')
cv.namedWindow('HSV Frame')
cv.createTrackbar('Low H', 'HSV Frame' , low_H, 180, low_H_trackbar)
cv.createTrackbar('High H', 'HSV Frame' , high_H, 180, high_H_trackbar)
cv.createTrackbar('Low S', 'HSV Frame' , low_S, 255, low_S_trackbar)
cv.createTrackbar('High S', 'HSV Frame' , high_S, 255, high_S_trackbar)
cv.createTrackbar('Low V', 'HSV Frame' , low_V, 255, low_V_trackbar)
cv.createTrackbar('High V', 'HSV Frame' , high_V, 255, high_V_trackbar)

while True:
    
    ret, img = cap.read()
    if img is None:
        break
    frame_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    
    
    cv.imshow('Captured Video', img)
    cv.imshow('HSV Frame', frame_threshold)
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

vid.release()
cv.destroyAllWindows()
