import cv2

cap = cv2.VideoCapture(0)

object_detector = cv2.createBackgroundSubtractorMOG2(varThreshold=5)
while True :
    ret, frame = cap.read()
    height,width = frame.shape[:2]
    
    roi =frame[160:300,100:340]
    
    mask = object_detector.apply(roi)
    
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        # cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),3)
    
    cv2.imshow('Roi',roi)
    cv2.imshow('Frame',frame)
    cv2.imshow('Mask',mask)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
print('종료')