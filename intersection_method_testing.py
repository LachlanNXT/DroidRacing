import numpy as np
import cv2
import config
import time

def chromaticity(image):
    B = image[:, :, 0].astype(np.uint16)
    G = image[:, :, 1].astype(np.uint16)
    R = image[:, :, 2].astype(np.uint16)    
    Y = 255.0 / (B + G + R)
    b = (B * Y).astype(np.uint8)
    g = (G * Y).astype(np.uint8)
    r = (R * Y).astype(np.uint8)
    return cv2.merge((b,g,r))

def colour_threshold(image, low, high):
    return cv2.inRange(image, np.array(low), np.array(high))

def line_coefs(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / float(D)
        y = Dy / float(D)
        return x,y
    else:
        return False

# load image
raw_im = cv2.imread("test_image_20.jpg")
# make image smaller
h, w = raw_im.shape[:2]
raw_im = cv2.resize(raw_im, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
h, w = raw_im.shape[:2]
# extract ROI
raw_im = raw_im[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
h, w = raw_im.shape[:2]

while (1):
    im = raw_im.copy()
    
    # colour thresholding
    chroma = chromaticity(im)
    blue_mask = colour_threshold(chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)
    yellow_mask = colour_threshold(chroma, config.YELLOW_CHROMA_LOW, config.YELLOW_CHROMA_HIGH)
    colour_mask = cv2.bitwise_or(blue_mask, yellow_mask)
    cv2.imshow("colour_mask with noise", colour_mask)
    colour_mask = cv2.erode(colour_mask, np.ones((2,2), np.uint8))
    colour_mask = cv2.dilate(colour_mask, np.ones((5,5), np.uint8))

    # lines
    lines = cv2.HoughLinesP(colour_mask, config.HOUGH_LIN_RES, config.HOUGH_ROT_RES, config.HOUGH_VOTES, config.HOUGH_MIN_LEN, config.HOUGH_MAX_GAP)
    
    yellow = np.zeros(4, np.int32)
    blue = np.zeros(4, np.int32)
    yellow_n = 0
    blue_n = 0
    if lines != None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
            if config.MIN_LINE_ANGLE < abs(angle) < config.MAX_LINE_ANGLE:
                if angle > 0:
                    yellow += line[0]
                    yellow_n += 1
                elif angle < 0:
                    blue += line[0]
                    blue_n += 1
                if config.IMSHOW:
                    cv2.line(im, (x1,y1), (x2,y2), (0,0,255), 1)

    if yellow_n > 0:
        yellow /= yellow_n
    else:
        yellow = np.array([978, 76, 1003, 90]) # replace with last_yellow

    if blue_n > 0:
        blue /= blue_n
    else:
        blue = np.array([99, 94, 130, 76]) # replace with last_blue

    yellow_line = line_coefs(yellow[:2], yellow[2:])
    blue_line = line_coefs(blue[:2], blue[2:])
    inter = intersection(blue_line, yellow_line)
    if inter:
        centre = int(inter[0])

    cv2.line(im, tuple(yellow[:2]), tuple(yellow[2:]), (0, 255, 0), 2)
    cv2.line(im, tuple(blue[:2]), tuple(blue[2:]), (0, 255, 0), 2)
    cv2.circle(im, (centre, h - 20), 10, (255,0,0), -1)
    cv2.imshow("im", im)
    cv2.imshow("color_mask without noise", colour_mask)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()