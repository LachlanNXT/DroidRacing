import numpy as np
import cv2
import config
import time

def chromaticity(image):
    image = image.astype(np.uint16)
    h,w = image.shape[:2]
    B = image[:, :, 0]
    G = image[:, :, 1]
    R = image[:, :, 2]
    Y = (B + G + R).astype(float)
    b = B / Y
    g = G / Y
    r = R / Y
    image = np.zeros((h, w, 3), np.uint8)
    image[:, :, 0] = b * 255
    image[:, :, 1] = g * 255
    image[:, :, 2] = r * 255
    return image

def colour_threshold(image, low, high):
    return cv2.inRange(image, np.array(low), np.array(high))

def callback(x):
    pass

# load image
raw_im = cv2.imread("test_image_4.jpg")
# make image smaller
h, w = raw_im.shape[:2]
raw_im = cv2.resize(raw_im, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
h, w = raw_im.shape[:2]
# extract ROI
raw_im = raw_im[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
h, w = raw_im.shape[:2]

while (1):
    im = raw_im.copy()

    # edge detection
    #edges = cv2.Canny(im, CannyMin, CannyMax, apertureSize=3)
    
    # colour thresholding
    chroma = chromaticity(im)
    blue_mask = colour_threshold(chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)
    yellow_mask = colour_threshold(chroma, config.YELLOW_CHROMA_LOW, config.YELLOW_CHROMA_HIGH)
    colour_mask = cv2.bitwise_or(blue_mask, yellow_mask)
    cv2.imshow("colour_mask with noise", colour_mask)
    #colour_mask = cv2.medianBlur(colour_mask, 3)
    #colour_mask = cv2.morphologyEx(colour_mask, cv2.MORPH_OPEN, np.ones((2,2), np.uint8))
    colour_mask = cv2.erode(colour_mask, np.ones((2,2), np.uint8))
    colour_mask = cv2.dilate(colour_mask, np.ones((5,5), np.uint8))

    # line detection
    lines = cv2.HoughLinesP(colour_mask, config.HOUGH_LIN_RES, config.HOUGH_ROT_RES, config.HOUGH_VOTES, config.HOUGH_MIN_LEN, config.HOUGH_MAX_GAP)
    line_x_hist = np.transpose(np.vstack((lines[:,:,0], lines[:,:,2])))[0]

    # histogram 
    hist = colour_mask.sum(axis=0)

    # show colour mask histogram
    # for i in range(len(hist)):
    #     cv2.line(im, (i, h), (i, h-(hist[i]/50)), (255,0,0), 1)

    # show lines from HoughLines
    blue_lines = np.array([])
    yellow_lines = np.array([])
    if lines != None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
            if angle > 0:
                yellow_lines = np.append(yellow_lines, [x1, x2])
            elif angle < 0:
                blue_lines = np.append(blue_lines, [x1, x2])
            if 20 < abs(angle) < 90:
                cv2.line(im, (x1,y1), (x2,y2), (0,0,255), 2)

    last_yellow_mean = 990
    last_blue_mean = 120

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