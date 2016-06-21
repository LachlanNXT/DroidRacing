import numpy as np
import cv2
import config

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

window_name = "Vision Testing"
cv2.namedWindow(window_name)
cv2.createTrackbar('CannyMin', window_name, 1, 1000, callback)
cv2.createTrackbar('CannyMax', window_name, 1, 1000, callback)
cv2.createTrackbar('HoughLinRes', window_name, 1, 500, callback)
cv2.createTrackbar('HoughRotRes', window_name, 1, 180, callback)
cv2.createTrackbar('HoughVotes', window_name, 1, 1000, callback)
cv2.createTrackbar('HoughMinLen', window_name, 0, 50, callback)
cv2.createTrackbar('HoughMaxGap', window_name, 0, 50, callback)

# load image
raw_im = cv2.imread("test_image_5.jpg")
# make image smaller
h, w = raw_im.shape[:2]
raw_im = cv2.resize(raw_im, (w/3, h/3), interpolation = cv2.INTER_LINEAR)
h, w = raw_im.shape[:2]
# extract ROI
raw_im = raw_im[int(0.4*h):int(0.6*h), :]

while (1):
    CannyMin =  cv2.getTrackbarPos('CannyMin', window_name)
    CannyMax =  cv2.getTrackbarPos('CannyMax', window_name)
    HoughLinRes =  cv2.getTrackbarPos('HoughLinRes', window_name)
    HoughRotRes =  cv2.getTrackbarPos('HoughRotRes', window_name)
    HoughVotes =  cv2.getTrackbarPos('HoughVotes', window_name)
    HoughMinLen =  cv2.getTrackbarPos('HoughMinLen', window_name)
    HoughMaxGap =  cv2.getTrackbarPos('HoughMaxGap', window_name)

    im = raw_im.copy()

    # edge detection
    #edges = cv2.Canny(im, CannyMin, CannyMax, apertureSize=3)

    chroma = chromaticity(im)
    edges = colour_threshold(chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)

    # line detection
    lines = cv2.HoughLinesP(edges, HoughLinRes, np.pi/HoughRotRes, HoughVotes, minLineLength=HoughMinLen, maxLineGap=HoughMaxGap)

    # display results
    if lines != None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(im, (x1,y1), (x2,y2), (0,0,255), 2)
    cv2.imshow(window_name, im)
    cv2.imshow("edges", edges)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()