import numpy as np
import cv2
import math
Lane_D = 7 ## Lane' Detecting Length
Section = 2 ## 
width = 640 ## frame Width
height = 480 ## frame Height
check_w = int(width/2) ## Center Point
Roi_h = 0.1 ## ROI's Height and Cut Height's Length
pi = 3.141592
d_check = 5

## width = 640 height = 480


def image_LAB(img):  ## Using the LAB_Convert,correction image's Light
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


def resize(image):  ## roi resize the roi's size
    h, w = image.shape[:2]
    d_h = int(h * Roi_h)  ## roi's image'height
    pts_src = np.array([[0, h * 0.85], [w, h * 0.85], [w, h * 0.95], [0, h * 0.95]],
                       dtype=np.float32)  ##roi Section's pts
    pts_dst = np.array([[0, 1], [w, 1], [w, 1 + d_h], [0, 1 + d_h]], dtype=np.float32)  ## resize Section's pts
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)  ## Get a Warping Point Matrix
    dst = cv2.warpPerspective(image, M, (w, h))  ## ROI Image Warping Complete image
    crop = dst[0:d_h, 0:width]
    return crop


def Classfication(image):
    lower_w = np.array([0, 220, 0]) ## HLS White Low Value
    higher_w = np.array([179, 255, 255]) ## HLS White High Value
    img = cv2.GaussianBlur(image, (5, 5), 0) ## Image Blur
    ret, image = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) ## image Threshold
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS) ## Convert HLS Color
    final = cv2.inRange(hls, lower_w, higher_w) ## Detecting White Value from image
    final = cv2.erode(final, (5, 5), iterations=3) ## erode
    final = cv2.dilate(final, (5, 5), iterations=5) ## dilate > Use the image Openning for Delete noise
    return final ## return the Binary image


def ROI(image):
    pt1 = (width * 0, height * 0.85)  ## ROI's Left_H Point
    pt2 = (width * 1.0, height * 0.85)  ## ROI's Right_H Point
    pt3 = (width, height * 0.95)  ## ROI's Right_L Point
    pt4 = (0, height * 0.95)  ## ROI's Left_L Point
    #print("L_H : ",pt1,"R_H",pt2,"R_L",pt3,"L_L",pt4,"\n")
    roi_corner = np.array([[pt1, pt2, pt3, pt4]], dtype=np.int32)  ## ROi Point array
    return roi_corner


def polyROI(image, points):  ## Original Image's ROI
    if len(image.shape) == 2: ## if input image is 1Channel
        channels = 1
    else: ## input image is Not 1Channel
        channels = image.shape[2]
    mask = np.zeros_like(image) ## Create Mask Same Size input Image
    ignore_mask_color = (255,) * channels ## Mask's Value All 255
    cv2.fillPoly(mask, points, ignore_mask_color) ## Mask Create
    return cv2.bitwise_and(image, mask) ## Mask  and Image Crop the pixel'value over 255


def L_Line(image):  ## Create Left_Lane's Point Array_for Section
    Left_Line = []
    S_H = 10
    E_H = int(height * Roi_h)-1
    flag = 1
    increase = int((E_H - S_H) / (Section-1))-1
    for i in range(E_H,S_H, -increase):
        a = l_detect(image,check_w,i)
        flag = flag + 1
        if (flag > Section):  ## if Wanted Section was arrived, flag's Value = 0, escape this Function
            #Left_Line.append([a, i])
            Left_Line.append([a,i])
            final_L = np.vstack(Left_Line)
            return final_L
        else:
            Left_Line.append([a, i])

def R_Line(image):  ## Create Right_Lane's Point Array_for Section
    Right_Line = []
    S_H = 10
    E_H = int(height * Roi_h)-1
    flag = 1
    increase = int((E_H - S_H) / (Section-1))-1
    for i in range(E_H, S_H, -increase):
        a = r_detect(image, check_w, i)
        flag = flag + 1
        if (flag > Section):
            Right_Line.append([a, i])
            final_R = np.vstack(Right_Line)
            return final_R
        else:
            Right_Line.append([a, i])

def l_detect(image,w,h):
    flag = 1
    if(w > (Lane_D*2)):
        if (image[h][w] > 0):
            check,xx = check_l(image, w, h, flag)
            if (check>0):
                return w
            else:
                return l_detect(image,w-xx,h)
        else:
            return l_detect(image,w-1,h)
    else:
        check = int(check_w/2)
        return check

def r_detect(image, w, h):
    flag = 1
    if(w < width-(Lane_D*2)):
        if (image[h][w] > 0):
            check,xx = check_r(image, w, h, flag)
            if (check>0):
                return w
            else:
                return r_detect(image,w+xx,h)
        else:
            return r_detect(image,w+1,h)
    else:
        check = check_w + int(check_w/2)
        return check

def check_l(image, i, h, flag): 
    if(flag == Lane_D):
        check =1
        return check, flag
    else:
        if (image[h][i] >= 1):
            return check_l(image,i-1,h,flag+1)
        else:
            check = 0
            return check,flag
            
def check_r(image, i, h,flag):
    if(flag == Lane_D):
        check =1
        return check, flag
    else:
        if (image[h][i] >= 1):
            return check_r(image,i+1,h,flag+1)
        else:
            check = 0
            return check,flag
def Center_P(r_p, l_p):
    Center_P = [] ## Center Point array
    for i in range(Section):
        l_x = l_p[i][0]
        r_x = r_p[i][0]
        c_y = l_p[i][1]
        c_x = (l_x + r_x) / 2 ## Center Y_Point
        Center_P.append([c_x, c_y])
    Center_P = np.int_(Center_P) ## Casting Integer
    Center_P = np.vstack(Center_P) ## array Change the Vstack
    return Center_P

def create_pts(pts):
    pts_re = np.array([[0, 0], [0, 0]])
    pts_re[0] = pts[0]
    pts_re[1] = pts[1]
    return pts_re

def draw_circle(image, d_p):  ## Checking the Lane's Points's Correct
    Draw = image.copy()
    for i in range(Section):
        x = d_p[i][0]  ## Lane's X_Point
        y = d_p[i][1]  ## Lane's Y_Point
        cv2.circle(Draw, (x, y), 10, (255, 0, 0), -1)  ## Drawing Circle at Point
    return Draw

def slope(v1):
    x = v1[1][0] - v1[0][0]
    y = v1[0][1] - v1[1][1]
    radi = math.atan2(x, y)
    deg = int(radi * (180 / pi) / 3)
    degree = int((28-deg)/4)
    return degree

##Check the now's Degree is OverDegree
def slope_Check(now,before):
    if(before == now):
        return now, before
    else:
        if(((before - now) < -d_check)|((before - now) > d_check)):
            return before, before
        else:
            return now, before

def remap(image, v1, v2):
    Height = int(height * 0.85)
    for i in range(Section):
        v1[i][1] = v1[i][1] + Height
        v2[i][1] = v2[i][1] + Height
    return v1, v2

def stop(mask, speed):  ## Checking the Stop Lane
    b_s = speed
    d_h = int(height / 2)
    mask_2 = mask[0:d_h, 0:width]
    a = np.count_nonzero(mask_2)  ## 'a' is Detecting lane or hls's array
    thresh = int((width * d_h) * 0.3)  ## thresh is Stop_lane's Minimum size
    if ((a >= thresh) | (a < 150)):  ## Detecting Value is over the thresh
        speed = 0  ## Return the speed value is 0 (0 = Stop)
    else:  ## but Don't Over thresh
        speed = 1  ## Return the speed value is 1
    return speed, b_s
