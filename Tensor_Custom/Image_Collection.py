import tensorflow as tf
import uuid
import os
import time
import cv2

labels = ['bottle2']
number_imgs = 20

IMAGES_PATH = os.path.join('Tensorflow','workspace','images','collectedImages')

if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.makedirs(IMAGES_PATH)
    if os.name =='nt':
        os.makedirs(IMAGES_PATH)
for label in labels:
    path = os.path.join(IMAGES_PATH,label)
    if not os.path.exists(path):
        os.makedirs(path)
for label in labels:
    index = 0;
    cap = cv2.VideoCapture(0)
    print('Collecting Image for {}'.format(label))
    while index<10:
        print('Waiting for Ready Time')
        time.sleep(2)
        print('Capture {}!!'.format(label))
        ret,frame = cap.read()
        imgname = os.path.join(IMAGES_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname,frame)
        cv2.imshow('frame',frame)
        time.sleep(2)
        index+=1
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()