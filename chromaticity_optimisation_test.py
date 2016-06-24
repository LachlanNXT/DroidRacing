import cv2
import numpy as np
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

raw_im = cv2.imread("test_image_8.jpg")
h, w = raw_im.shape[:2]
raw_im = cv2.resize(raw_im, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
h, w = raw_im.shape[:2]
raw_im = raw_im[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
h,w = raw_im.shape[:2]

n = 500.0
avg = 0.0
for x in range(int(n)):
    start = time.clock()
    im = chromaticity(raw_im)
    end = time.clock()
    avg += (end-start) / n


print(str(avg) + " seconds")

cv2.imshow("chroma", im)
cv2.waitKey()
cv2.destroyAllWindows()