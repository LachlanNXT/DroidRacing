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
raw_im = cv2.imread("test_image_8.jpg")
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

    # line detection
    lines = cv2.HoughLinesP(colour_mask, config.HOUGH_LIN_RES, config.HOUGH_ROT_RES, config.HOUGH_VOTES, config.HOUGH_MIN_LEN, config.HOUGH_MAX_GAP)

    # show lines from HoughLines
    sum_blue_angle = 0.0
    sum_yellow_angle = 0.0
    num_blue_angles = 0
    num_yellow_angles = 0
    if lines.shape[0] > 0:
        for n in range()
            x1,y1,x2,y2 = line[0]
            angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
            if angle > 0:
                sum_yellow_angle += abs(angle)
                num_yellow_angles += 1
            elif angle < 0:
                sum_blue_angle += abs(angle)
                num_blue_angles += 1
            if 20 < abs(angle) < 90:
                cv2.line(im, (x1,y1), (x2,y2), (0,0,255), 2)

    last_yellow_mean = 20
    last_blue_mean = -20

    if len(blue_lines) and len(yellow_lines):
        centre = int(np.mean(blue_lines) + np.mean(yellow_lines)) / 2
    elif len(blue_lines):
        centre = int(np.mean(blue_lines) + last_yellow_mean) / 2
    else:
        centre = int(last_blue_mean + np.mean(yellow_lines)) / 2
    cv2.circle(im, (centre, h - 20), 10, (0,0,255), -1)

    cv2.imshow("im", im)
    cv2.imshow("color_mask without noise", colour_mask)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()