#!/usr/bin/env python
from Custom_F import *
import cv2
import numpy as np
import time

Degree_b = 0
widhth = 640
check_w = width/2
cap = cv2.VideoCapture("../../../001.avi")

while(cap.isOpened()):
    start = time.time()
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    Gu = cv2.UMat(frame)
    image = Gu.get()
    lab = image_LAB(image)
    pts = ROI(lab)
    roi = polyROI(lab,pts)
    hls = Classfication(roi)
    rs = resize(hls)
    left = L_Line(rs)
    right = R_Line(rs)
    center = Center_P(right,left)
    draw = draw_circle(rs,center)
    degree = slope(center)
    print("Now's Lane's Degree is ",degree)
    cv2.imshow("Center",draw)
    cv2.imshow("rs",rs)
    if(cv2.waitKey(1)==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
