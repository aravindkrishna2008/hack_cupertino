import cv2
import numpy as np
import time
import math

def drawline(img, pt1, pt2, color, thickness=1, style='dotted', gap=20):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in  np.arange(0,dist,gap):
        r = i/dist
        x = int((pt1[0]*(1-r)+pt2[0]*r) + .5)
        y = int((pt1[1]*(1-r)+pt2[1]*r) + .5)
        p = (x,y)
        pts.append(p)

    if style == 'dotted':
        for p in pts:
            cv2.circle(img,p,thickness,color,-1)
    else:
        s = pts[0]
        e = pts[0]
        i = 0
        for p in pts:
            s = e
            e = p
            if i % 2 == 1:
                cv2.line(img, s, e, color, thickness)
            i += 1

def get_crossing(frame):
    orig_frame = cv2.resize(frame, (204, 360))

    frame = orig_frame[120:244]

    lower = np.array([170, 170, 170]) 
    upper = np.array([230, 230, 230])

    mask = cv2.inRange(frame, lower, upper) 
    result = cv2.bitwise_and(frame, frame, mask = mask) 

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    kernel_size = 25
    blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    low_t = 50
    high_t = 150

    center_x = 0
    num = 0

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            if (blur[i][j] > 90):
                num += 1
                orig_frame[i+120][j] = (0, 255, 0)
                center_x += j
    center_x /= num

    drawline(orig_frame, [int(center_x), 140], [int(center_x), orig_frame.shape[0]], (0, 0, 255), 3)


    crosswalk_visible = True

    # edges = cv2.Canny(blur, low_t, high_t)

    # # binary = cv2.bitwise_and(blur, blur)

    # crosswalk_visible = False
    # crosswalk_location = [[0, 0], [0, 0]]

    # (contours,_) = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # for contour in contours:
    #     min_rect = cv2.minAreaRect(contour)

    #     box = cv2.boxPoints(min_rect)
    #     box = np.int0(box)

    #     y = abs(box[2][1] - box[0][1])
    #     x = abs(box[2][0] - box[0][0])
        

    #     if (y/max(1, x) > 1 and y > 10):
    #         cv2.line(orig_frame, [box[0][0] - 5, box[0][1] + 120], [box[2][0], box[2][1] + 240], (0, 255, 0), 10)
    #         crosswalk_visible = True
    #         crosswalk_location = [[box[0][0] - 5, box[0][1] + 120], [box[2][0], box[2][1] + 240]]
    #         break
    
    return crosswalk_visible, orig_frame


if __name__ == '__main__':
    path = "C:\\Users\\knott\\2024-hack-cupertino-proj\\IMG_0159.MOV"
    vid = cv2.VideoCapture(path)

    while vid.isOpened():
        _, frame = vid.read()

        _, frame = get_crossing(frame)

        cv2.imshow("FRAME", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

# print(get_crossing("./temp.jpg"))