import ctypes
import numpy as np
import cv2
import time

lib = ctypes.cdll.LoadLibrary('/home/pi/libchromaticity.so')
chromaticity = lib.chromaticity

image = cv2.imread("test_image_13.jpg")
h, w = image.shape[:2]
image = cv2.resize(image, (w/2, h/2), interpolation = cv2.INTER_LINEAR)
h, w = image.shape[:2]
image = image[int(0.4*h):int(0.55*h), int(0.1*w):int(0.9*w)]
h, w = image.shape[:2]

size = int(h*w*4)
size = ctypes.c_int(size)
imagep = ctypes.c_void_p(image.ctypes.data)

start = time.clock()
chromaticity(imagep, size)
end = time.clock()
print((end-start) * 1000)

cv2.imshow("Chromaticity", image)
cv2.waitKey()