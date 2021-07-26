import cv2

img = cv2.imread('../../../steer_arrow.png')
cv2.imshow('arrow',img)
cv2.waitKey(0)

cv2.destroyAllWindows()