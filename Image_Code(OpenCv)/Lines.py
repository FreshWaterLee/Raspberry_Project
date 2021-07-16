#import rospy
import numpy as np
import cv2, random, math, time
# 영상 사이즈는 가로세로 640 x 480
Width = 640
Height = 480
# ROI 영역 : 세로 420 ~ 460 만큼 잘라서 사용
Offset = 420
Gap = 40
# draw lines
def draw_lines(img, lines):
    global Offset
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 허프변환 함수로 검출된 모든 선분을 알록달록하게 출력
        color = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        img = cv2.line(img, (x1, y1 + Offset), (x2, y2+Offset), color, 2)
    return img

  # draw rectangle

def draw_rectangle(img, lpos, rpos, offset=0):
    center = int((lpos + rpos)/2)
    cv2.rectangle(img, (lpos - 5, 15 + offset), (lpos + 5, 25 + offset), (0, 255, 0), 2)
    cv2.rectangle(img, (rpos - 5, 15 + offset), (rpos + 5, 25 + offset), (0, 255, 0), 2)
    cv2.rectangle(img, (center - 5, 15 + offset), (center + 5, 25 + offset), (0, 255, 0), 2)
    cv2.rectangle(img, (315, 15 + offset), (325, 25 + offset), (0, 0, 255), 2)
    return img

def divide_left_right(lines):
    global Width
    # 기울기 절대값이 0 ~ 10 인것만 추출
    low_slope_threshold = 0
    high_slope_threshold = 10
    slopes = []
    new_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 == 0:
            slope = 0
        else:
            slope = float(y2 - y1) / float(x2 - x1)
        if(abs(slope) > low_slope_threshold) and (abs(slope) < high_slope_threshold):
            slopes.append(slope)
            new_lines.append(line[0])
    left_lines = []
    right_lines = []
    for j in range(len(slopes)):
        Line = new_lines[j]
        slope = slopes[j]
        x1, y1, x2, y2 = Line
        # 화면에 왼쪽/오른쪽에 있는 선분 중에서 기울기가 음수 / 양수 인것들만 모음
        if(slope < 0) and (x2 < Width/2 - 90):
            left_lines.append([Line.tolist()])
        elif (slope > 0) and (x1 > Width/2 + 90):
            right_lines.append([Line.tolist()])
    return left_lines, right_lines

# 기울기와 y절편의 평균값 구하기
def get_line_params(lines):
    # sum of x, y, m
    x_sum = 0.0
    y_sum = 0.0
    m_sum = 0.0
    size = len(lines)
    if size == 0:
        return 0, 0
    for line in lines:
        x1, y1, x2, y2 = line[0]   
        x_sum += x1 + x2
        y_sum += y1 + y2
        m_sum += float(y2 - y1) / float(x2 - x1)
    x_avg = x_sum / (size * 2)
    y_avg = y_sum / (size * 2)
    m = m_sum / size
    b = y_avg - m * x_avg
    return m, b


def get_line_pos(img, lines, left=False, right=False):
    global Width, Height
    global Offset, Gap
    m, b = get_line_params(lines)
    if m == 0 and b == 0:
        if left :
            pos = 0
        if right :
            pos = Width
    else:
        y = Gap / 2
        pos = (y - b) / m
        b += Offset
        x1 = (Height - b) /float(m)
        x2 = ((Height/2) - b) / float(m)
        cv2.line(img, (int(x1), Height), (int(x2), int(Height/2)), (255,0,0), 3)
    return img,int(pos)

def process_image(frame):
    global Width
    global Offset, Gap
    # gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    # canny edge
    low_threshold = 60
    high_threshold = 70
    edge_img = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold)
    # HoughLinesP
    roi = edge_img[Offset : Offset+Gap, 0 : Width]
    all_lines = cv2.HoughLinesP(roi, 1, math.pi/180, 30,30,10)
    if all_lines is None:
        return 0, 640
    left_lines,right_lines = divide_left_right(all_lines)
    frame, lpos = get_line_pos(frame, left_lines, left=True)
    frame, rpos = get_line_pos(frame, right_lines, right=True)
    frame = draw_lines(frame, left_lines)
    frame = draw_lines(frame, right_lines)
    frame = cv2.line(frame, (230,235), (410, 235), (255,255,255), 2)
    # draw rectangle
    frame = draw_rectangle(frame, lpos, rpos, offset=Offset)
    return (lpos, rpos), frame

def draw_steer(image, steer_angle):
    global Width, Height, arrow_pic
    arrow_pic = cv2.imread('../../steer_arrow2.png', cv2.IMREAD_COLOR)
    origin_Height = arrow_pic.shape[0]
    origin_Width = arrow_pic.shape[1]
    steer_wheel_center = int(origin_Height * 0.74)
    arrow_Height = int(Height/2)
    arrow_Width = int((arrow_Height * 462)/728)

    matrix = cv2.getRotationMatrix2D((origin_Width/2, steer_wheel_center), (steer_angle) * 2.5, 0.7)    
    arrow_pic = cv2.warpAffine(arrow_pic, matrix, (origin_Width+60, origin_Height))
    arrow_pic = cv2.resize(arrow_pic, dsize=(arrow_Width, arrow_Height), interpolation=cv2.INTER_AREA)
    gray_arrow = cv2.cvtColor(arrow_pic, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_arrow, 1, 255, cv2.THRESH_BINARY_INV)

    arrow_roi = image[arrow_Height: Height, int((Width/2 - arrow_Width/2)) : int((Width/2 + arrow_Width/2))]
    arrow_roi = cv2.add(arrow_pic, arrow_roi, mask=mask)
    res = cv2.add(arrow_roi, arrow_pic)
    image[(Height - arrow_Height): Height, int(Width/2 - arrow_Width/2): int(Width/2 + arrow_Width/2)] = res
    cv2.imshow('steer', image)

def start():
    global image, Width, Height
    cap = cv2.VideoCapture('../../001.avi')
    while cap.isOpened():
        ret, image = cap.read()
        image = cv2.resize(image,dsize=(640,480),interpolation=cv2.INTER_AREA)
        ##time.sleep(0.03)        
        pos, frame = process_image(image)
        #frame = process_image(image)
        center = (pos[0] + pos[1]) / 2        
        angle = 320 - center
        steer_angle = angle * 0.4
        draw_steer(frame, steer_angle)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    start()
