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

i=1
while (1):
    # load image
    raw_im = cv2.imread("test_image_%d.jpg" % i)
    # make image smaller
    h, w = raw_im.shape[:2]
    raw_im = cv2.resize(raw_im, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
    h, w = raw_im.shape[:2]
    # extract ROI
    raw_im = raw_im[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
    h, w = raw_im.shape[:2]

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
    
    yellow_angle = 0
    blue_angle = 0
    yellow_n = 0
    blue_n = 0
    if lines != None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))
            if config.MIN_LINE_ANGLE < abs(angle) < config.MAX_LINE_ANGLE:
                if angle > 0:
                    yellow_angle += abs(angle)
                    yellow_n += 1
                elif angle < 0:
                    blue_angle += abs(angle)
                    blue_n += 1
                if config.IMSHOW:
                    cv2.line(im, (x1,y1), (x2,y2), (0,0,255), 1)

    if yellow_n > 0:
        yellow_angle /= yellow_n
    else:
        yellow_angle = 25 # replace with last_yellow

    if blue_n > 0:
        blue_angle /= blue_n
    else:
        blue_angle = 25 # replace with last_blue

    centre = abs(yellow_angle - blue_angle)
    if blue_angle < yellow_angle:
        centre = -centre

    steering = ((centre/30.0)+1)/2
    if steering > 1:
        steering = 1.0
    if steering < 0:
        steering = 0.0

    print "blue:",blue_angle, "yellow:",yellow_angle,"centre:", centre, "steering:", steering

    cv2.line(im, (w/2, h-20), ((w/2), h-120), (255,255,255), 2)
    cv2.line(im, (w/2, h-20), ((w/2)+int(100*np.cos(np.deg2rad(centre+90))), int((h-20)-100*np.sin(np.deg2rad(centre+90)))), (0,255,0), 2)
    #cv2.circle(im, (int(centre), h - 20), 10, (255,0,0), -1)
    cv2.imshow("im", im)
    cv2.imshow("color_mask without noise", colour_mask)
    if cv2.waitKey(2000) & 0xFF == 27:
        break

    i += 1
    if i == 22:
        i = 24
    if i > 38:
        break

cv2.destroyAllWindows()