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

# load image
raw_im = cv2.imread("test_image_4.jpg")
# make image smaller
h, w = raw_im.shape[:2]
raw_im = cv2.resize(raw_im, (w/3, h/3), interpolation = cv2.INTER_LINEAR)
h, w = raw_im.shape[:2]
# extract ROI
raw_im = raw_im[int(0.4*h):int(0.6*h), :]

chroma = chromaticity(raw_im)
blue_mask = colour_threshold(chroma, config.BLUE_CHROMA_LOW, config.BLUE_CHROMA_HIGH)
yellow_mask = colour_threshold(chroma, config.YELLOW_CHROMA_LOW, config.YELLOW_CHROMA_HIGH)

cv2.imshow("blue mask | yellow mask", np.hstack((blue_mask, yellow_mask)))
cv2.imshow("Chromaticity", chroma)
cv2.waitKey()