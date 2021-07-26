import cv2
import numpy as np
import sys
#import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
fps = cap.get(cv2.CAP_PROP_FPS)
kernel = np.ones((5,5),np.uint8)
#print("Frames per second using video.get(cv2.CAP_PROP_FPS): {0}".format(fps))

while True:
    ret, image = cap.read()
    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img_gray,(7,7),0)
    Canny = cv2.Canny(imgBlur,100,100)
    imgDia = cv2.dilate(Canny,kernel,iterations=1)
    imgEro = cv2.erode(imgDia,kernel,iterations=1)
    
    cv2.imshow('Image', Canny)
    cv2.imshow('Dialation', imgDia)
    cv2.imshow('Eroded', imgEro)
    if cv2.waitKey(30) > 0:
        break

cv2.destroyAllWindows()