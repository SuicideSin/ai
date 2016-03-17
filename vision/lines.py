#!/usr/local/bin/python3
import numpy as np
import random
from matplotlib import pyplot as plt
import urllib.request, cv2, sys, re, time, math

# Default image file
imgSpec = "duck.jpg"
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



def toGray(img):    
    gray = np.zeros((height,width,3), np.uint8)
    for i in range(height):
        for j in range(width):
            gray[i, j] = np.dot(grayscale, img[i, j])
    return gray

def blur(img):
    blurred = cv2.filter2D(img, -1, gauss)
    #blurred = filter(img, gauss)
    return blurred 

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    
    if len(sys.argv) > 3:
        edged = cv2.Canny(image, int(sys.argv[2])**(1/2), int(sys.argv[3])**(1/2))
    else:
        edged = cv2.Canny(image, lower, upper)

    return edged


gray = toGray(img.copy())
blurred = blur(gray.copy())
auto = auto_canny(blurred.copy())

canny = np.zeros((height,width,3), np.uint8)
canny[:,:] = 255
edges = set()
for r in range(1,height-1):
    for c in range(1,width-1):
        if auto[r, c] == 255:
            canny[r,c] = 0
            edges.add((r, c))

print("Height: {}\nWidth: {}\nEdge Pixels: {}".format(height,width,len(edges)))

hough = np.zeros((int(math.sqrt(height**2+width**2)),900,3), np.uint8)
hough[:,:] = 255

intersects = {(r, c): 0 for r in range(height) for c in range(width)}


lines = {}
for e in edges:
    i,j = e[0], e[1]
    r,c = i,j
    
    ø = 0
    while ø <= 180:
        rad = ø*math.pi/180
        pair = (c*np.cos(rad) + r*np.sin(rad), rad)
        hough[int(pair[0]),int(pair[1]*180/math.pi)] -= 1
        if pair in lines:
            lines[pair] += 1
        else:
            lines[pair] = 1
    
        #slope = -math.tan(rad+math.pi/2)
        
        ø+=.5




print("{}, {} times".format(max(lines, key=lines.get), lines[max(lines, key=lines.get)]))
del lines[max(lines, key=lines.get)]
print("{}, {} times".format(max(lines, key=lines.get), lines[max(lines, key=lines.get)]))


cv2.imshow('Hough', hough)
while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        break
    if key == ord('r'):
        cv2.destroyAllWindows()
        cv2.imshow('Original', img)
    if key == ord('g'):
        cv2.destroyAllWindows()
        cv2.imshow('Grayscale', gray)
    if key == ord('b'):
        cv2.destroyAllWindows()
        cv2.imshow('Gaussian Blur', blurred)
    if key == ord('e'):
        cv2.destroyAllWindows()
        cv2.imshow('Edges', canny)
    if key == ord('h'):
        cv2.destroyAllWindows()
        cv2.imshow('Hough', hough)