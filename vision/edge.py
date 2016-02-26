#!/usr/local/bin/python3
import numpy as np
import random
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
                      
def findNeighbors(t):
    i,j=t
    rowLimit = height-1
    columnLimit = width-1
    n = []
    for x in range(max(0, i-1), min(i+1, rowLimit)+1):
        for y in range(max(0, j-1), min(j+1, columnLimit)+1):
            if x != i or y != j:
                n.append((x,y))
    return n
    
def roundAngle(value):
    array = np.array([45, 90, -45, -90, 0])
    i = (np.abs(array-value)).argmin()
    return array[i]

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

def edges(img):
    
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 9000

    edges = np.zeros((height,width,3), np.uint8)
    edges[:,:] = 255
    
    for i in range(1,height-1):
        for j in range(1,width-1):
            Gx = -int(img[i-1,j+1][0]) + int(img[i+1,j+1][0]) + -2*int(img[i-1,j][0]) + 2*int(img[i+1,j][0]) + -int(img[i-1,j-1][0]) + int(img[i+1,j-1][0])
            Gy = int(img[i-1,j+1][0]) + 2*int(img[i,j+1][0]) + int(img[i+1,j+1][0]) + -int(img[i-1,j-1][0]) + -2*int(img[i,j-1][0]) + -int(img[i+1,j-1][0])
            
            if Gx**2 + Gy**2 > T:
                edges[i,j] = 0

    return edges
    
def canny1(img):

    T = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    
    edges = []
    pixels = {}
    
    cEdges = np.zeros((height,width,3), np.uint8)
    cEdges[:,:] = (255,255,255)
    
    for i in range(1,height-1):
        for j in range(1,width-1):
            Gx = -int(img[i-1,j+1][0]) + int(img[i+1,j+1][0]) + -2*int(img[i-1,j][0]) + 2*int(img[i+1,j][0]) + -int(img[i-1,j-1][0]) + int(img[i+1,j-1][0])
            Gy = int(img[i-1,j+1][0]) + 2*int(img[i,j+1][0]) + int(img[i+1,j+1][0]) + -int(img[i-1,j-1][0]) + -2*int(img[i,j-1][0]) + -int(img[i+1,j-1][0])
            g = Gx**2 + Gy**2
            pixels[(i,j)] = (Gx, Gy)
            if g > T:
                edges.append((i,j))
    
    for i in edges:
        angle = roundAngle(np.arctan2(pixels[i][1], pixels[i][0]) * 180 / np.pi) 
        
        x = i[0]
        y = i[1]
        
        if 1 < x < height-2 and 1 < y < width-2: 
        
            if angle == 0:
                x1,y1 = x+1,y
                x2,y2 = x-1,y
                
            if angle == 45:
                x1,y1 = x+1,y+1
                x2,y2 = x-1,y-1
            
            if angle == -45:
                x1,y1 = x+1,y-1
                x2,y2 = x-1,y+1
                
            if abs(angle) == 90:
                x1,y1 = x,y+1
                x2,y2 = x,y-1
            
            g = pixels[i][0]**2 + pixels[i][1]**2
            g1 = pixels[(x1,y1)][0]**2 + pixels[(x1,y1)][1]**2
            g2 = pixels[(x2,y2)][0]**2 + pixels[(x2,y2)][1]**2
            
            if g == max(g, g1, g2):
                cEdges[x,y] = 0

    return cEdges

def canny2(img):

    T = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    t = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
    
    edges = set()
    weak = set()
    pixels = {}
    
    cEdges = np.zeros((height,width,3), np.uint8)
    cEdges[:,:] = (255,255,255)
    
    for i in range(1,height-1):
        for j in range(1,width-1):
            Gx = -int(img[i-1,j+1][0]) + int(img[i+1,j+1][0]) + -2*int(img[i-1,j][0]) + 2*int(img[i+1,j][0]) + -int(img[i-1,j-1][0]) + int(img[i+1,j-1][0])
            Gy = int(img[i-1,j+1][0]) + 2*int(img[i,j+1][0]) + int(img[i+1,j+1][0]) + -int(img[i-1,j-1][0]) + -2*int(img[i,j-1][0]) + -int(img[i+1,j-1][0])
            g = Gx**2 + Gy**2
            pixels[(i,j)] = (Gx, Gy)
            if g > T:
                edges.add((i,j))
            elif t < g < T:
                weak.add((i,j))
    for i in weak:
        neighbors = findNeighbors(i)
        for n in neighbors:
            if n in edges:
                edges.add(i)
                
    for i in edges:
        angle = roundAngle(np.arctan2(pixels[i][1], pixels[i][0]) * 180 / np.pi) 
        
        x = i[0]
        y = i[1]
        
        if 1 < x < height-2 and 1 < y < width-2: 
        
            if angle == 0:
                x1,y1 = x+1,y
                x2,y2 = x-1,y
                
            if angle == 45:
                x1,y1 = x+1,y+1
                x2,y2 = x-1,y-1
            
            if angle == -45:
                x1,y1 = x+1,y-1
                x2,y2 = x-1,y+1
                
            if abs(angle) == 90:
                x1,y1 = x,y+1
                x2,y2 = x,y-1
            
            g = pixels[i][0]**2 + pixels[i][1]**2
            g1 = pixels[(x1,y1)][0]**2 + pixels[(x1,y1)][1]**2
            g2 = pixels[(x2,y2)][0]**2 + pixels[(x2,y2)][1]**2
            
            if g == max(g, g1, g2):
                cEdges[x,y] = 0

    return cEdges

cv2.imshow('Original', img)

grayed = toGray(img)
blurred = blur(grayed)
sobel = edges(blurred.copy())
can1 = canny1(blurred.copy())
can2 = canny2(blurred.copy())

def save():
    pimg = img.copy()
    psobel = sobel.copy()
    pcan1 = can1.copy()
    pcan2 = can2.copy()
    pics = [pimg, psobel, pcan1, pcan2]
    c = 0
    for pic in pics:
        c += 1
        for i in range(height):
            pic[i, 0] = 0
            pic[i, width-1] = 0
        for j in range(width):
            pic[0, j] = 0
            pic[height-1, j] = 0
        name = "{}{}".format(c, imgSpec[-4:])
        #print(name)
        cv2.imwrite(name,pic)

save()

pics = {"g":grayed, "b": blurred, "e": sobel, "c1": can1, "c2": can2}

while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        break
    if key == ord('r'):
        cv2.destroyAllWindows()
        cv2.imshow('Original', img)
        pics["b"] = blurred
    if key == ord('g'):
        cv2.destroyAllWindows()
        cv2.imshow('Grayscale', pics["g"])
    if key == ord('b'):
        cv2.destroyAllWindows()
        cv2.imshow('Gaussian Blur', pics["b"])
        pics["b"] = blur(pics["b"])
    if key == ord('e'):
        cv2.destroyAllWindows()
        cv2.imshow('Edges', pics["e"])
    if key == ord('c'):
        cv2.destroyAllWindows()
        cv2.imshow('Canny 1', pics["c1"])
    if key == ord('x'):
        cv2.destroyAllWindows()
        cv2.imshow('Canny 2', pics["c2"])
    if key == ord('v'):
        cv2.destroyAllWindows()
        cv2.imshow('wut', cv2.Canny(img,100,200))

