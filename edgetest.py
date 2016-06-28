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

def callback(x):
    pass

def auto_canny(image, sigma=0.30):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	return cv2.Canny(image, lower, upper)

while True:
    # load image
    n = raw_input("image number: ")
    raw_im = cv2.imread("test_image_%s.jpg" % n)
    # make image smaller
    h, w = raw_im.shape[:2]
    raw_im = cv2.resize(raw_im, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
    h, w = raw_im.shape[:2]
    # extract ROI
    raw_im = raw_im[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
    h, w = raw_im.shape[:2]

    im = raw_im.copy()

    # colour chromaticity
    chroma = np.power(chromaticity(im).astype(np.uint16), 2)
    chroma = (chroma / (255)).astype(np.uint8)
    cv2.imshow("chroma", chroma)
    chromaGray = cv2.cvtColor(chroma, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray", chromaGray)
    # edge detection
    edges = auto_canny(chroma)
    cv2.imshow("edges", edges)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(12,12))
    dilation = cv2.dilate(edges,kernel,iterations = 1)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    erode = cv2.erode(dilation,kernel,iterations = 1)
    erode = cv2.erode(erode,kernel2,iterations = 1)
    cv2.imshow("dilated", dilation)
    cv2.imshow("eroded", erode)
    if cv2.waitKey() & 0xFF == 27:
        break

cv2.destroyAllWindows()
