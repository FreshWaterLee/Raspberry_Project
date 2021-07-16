import cv2
cap = cv2.VideoCapture('../../001.avi')
arrow = cv2.imread('../../steer_arrow.png')
cv2.imshow('arrow',arrow)
cv2.waitKey(0)
print(cap.isOpened())
cv2.destroyAllWindows()
