#!/usr/local/bin/python3
import numpy as np
from matplotlib import pyplot as plt
import urllib.request, cv2, sys, re, time

# Default image file
imgSpec = "polarbear.jpg"
if len(sys.argv) > 1: imgSpec = sys.argv[1]


# Decide between file & url with regular expression (re)
if re.compile("^\\w*\\:\\/\\/").search(imgSpec) is None:
  img = cv2.imread(imgSpec, cv2.IMREAD_COLOR)
else:
  resp = urllib.request.urlopen(imgSpec)
  img = np.asarray(bytearray(resp.read()), dtype = "uint8")
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)


# Allows window to be resized by user (in theory)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
height, width = img.shape[:2]    # Get image dimensions
widthMax = 1024                  # The screen width, in pixels
if (width > widthMax):
  cv2.resizeWindow('image', widthMax, int(height*widthMax/width))

height, width, depth = img.shape

grayscale = np.array([0.3, 0.59, 0.11])

gauss = np.array([[1, 2, 1],
                  [2, 4, 2],
                  [1, 2, 1]])/16
                  
gradientx = np.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])

gradienty = np.array([[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]])

def toGray(img):    
    gray = np.zeros((height,width,3), np.uint8)
    for i in range(height):
        for j in range(width):
            gray[i, j] = np.dot(grayscale, img[i, j])
    return gray

def blur(img):
    blurred = cv2.filter2D(img, -1, gauss)
    return blurred

def edges(img):
    Gx = cv2.filter2D(img, -1, gradientx)

    Gy = cv2.filter2D(img, -1, gradienty)

    T = int(sys.argv[2])

    edges = img.copy()
    
    for i in range(height):
        for j in range(width):
            if Gx[i,j][0]**2 + Gy[i,j][0]**2 > T:
                edges[i,j] = 255
    
    return edges

cv2.imshow('Original', img)

grayed = toGray(img)
blurred = blur(grayed)

display = img.copy()

while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        break
    if key == ord('r'):
        cv2.destroyAllWindows()
        cv2.imshow('Original', img)
        display = img
    if key == ord('g'):
        cv2.destroyAllWindows()
        display = toGray(display)
        cv2.imshow('Grayscale', display)
    if key == ord('b'):
        cv2.destroyAllWindows()
        display = blur(display)
        cv2.imshow('Gaussian Blur', display)
    if key == ord('e'):
        cv2.destroyAllWindows()
        display = edges(display)
        cv2.imshow('Edges', display)
 
