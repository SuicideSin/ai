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
                  
gradientx = {0: [-1, 0, 1],
             1: [-2, 0, 2],
             2: [-1, 0, 1]}

gradienty = {0: [1, 2, 1],
             1: [0, 0, 0],
             2: [-1, -2, -1]}
                      
# def findNeighbors(i, j):
#     rowLimit = height-1
#     columnLimit = width-1
#     n = []
#     for x in range(max(0, i-1), min(i+1, rowLimit)+1):
#         for y in range(max(0, j-1), min(j+1, columnLimit)+1):
#             if x != i or y != j:
#                 n.append((x,y))
#     return n
    
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

def filter(img, dic):
    total = sum([sum(i) for i in dic.values()]) if sum([sum(i) for i in dic.values()]) > 0 else 1
    new = img.copy()
    for i in range(1,height-1):
        for j in range(1,width-1):
            new[i,j] = (dic[0][0]*int(img[i-1,j+1][0]) +
                        dic[0][1]*int(img[i,j+1][0]) +
                        dic[0][2]*int(img[i+1,j+1][0]) +
                        dic[1][0]*int(img[i-1,j][0]) +
                        dic[1][1]*int(img[i,j][0]) +
                        dic[1][2]*int(img[i+1,j][0]) +
                        dic[2][0]*int(img[i-1,j-1][0]) +
                        dic[2][1]*int(img[i,j-1][0]) +
                        dic[2][2]*int(img[i+1,j-1][0])) / total
    return new
    

def edges(img):
    
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 9000

    edges = img.copy()
    
    for i in range(1,height-1):
        for j in range(1,width-1):
            Gx = -int(img[i-1,j+1][0]) + int(img[i+1,j+1][0]) + -2*int(img[i-1,j][0]) + 2*int(img[i+1,j][0]) + -int(img[i-1,j-1][0]) + int(img[i+1,j-1][0])
            Gy = int(img[i-1,j+1][0]) + 2*int(img[i,j+1][0]) + int(img[i+1,j+1][0]) + -int(img[i-1,j-1][0]) + -2*int(img[i,j-1][0]) + -int(img[i+1,j-1][0])
            
            if Gx**2 + Gy**2 > T:
                edges[i,j] = 0
            else:
                edges[i,j] = 255

    return edges
    
def canny1(img):
    # Gx = cv2.filter2D(img, -1, gradientx)
    #
    # Gy = cv2.filter2D(img, -1, gradienty)

    T = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    
    edges = []
    pixels = {}
    
    cEdges = np.zeros((height,width,3), np.uint8)
    cEdges[:,:] = (255,255,255)
    
    for i in range(1,height-1):
        for j in range(1,width-1):
            Gx = -int(img[i-1,j+1][0]) + int(img[i+1,j+1][0]) + -2*int(img[i-1,j][0]) + 2*int(img[i+1,j][0]) + -int(img[i-1,j-1][0]) + int(img[i+1,j-1][0])
            Gy = int(img[i-1,j+1][0]) + 2*int(img[i,j+1][0]) + int(img[i+1,j+1][0]) + -int(img[i-1,j-1][0]) + -2*int(img[i,j-1][0]) + -int(img[i+1,j-1][0])
            
            pixels[(i,j)] = (Gx, Gy)
            g = Gx**2 + Gy**2
            if g > T:
                edges.append((i,j))
    
    for i in edges:
        #neighbors = findNeighbors(i[0],i[1]])
        angle = roundAngle(np.arctan2(pixels[i][1], pixels[i][0]) * 180 / np.pi) 
        
        x = i[0]
        y = i[1]
        
        if 1 < x < height-1 and 1 < y < width-1: 
        
            if angle == 0:
                x1,y1 = x+1,y
                x2,y2 = x-1,y
                
            if angle == -45:
                x1,y1 = x+1,y+1
                x2,y2 = x-1,y-1
            
            if angle == 45:
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
    Gx = cv2.filter2D(img, -1, gradientx)

    Gy = cv2.filter2D(img, -1, gradienty)

    T = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    
    lower = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    upper = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    
    edges = []
    pixels = {}
    
    cEdges = np.zeros((height,width,3), np.uint8)
    cEdges[:,:] = (255,255,255)
    
    for i in range(0,height):
        for j in range(0,width):
            g = Gx[i,j][0]**2 + Gy[i,j][0]**2
            pixels[(i,j)] = (Gx[i,j][0], Gy[i,j][1])
            if g > T:
                edges.append((i,j))
    
    for i in edges:
        #neighbors = findNeighbors(i[0],i[1]])
        angle = roundAngle(np.arctan2(pixels[i][1], pixels[i][0])* 180 / np.pi) 
        
        x = i[0]
        y = i[1]
        
        if 0 < x < height-1 and 0 < y < width-1: 
        
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

pics = {"g":grayed, "b": blurred, "e":edges(blurred.copy())}#, "c1":canny1(blurred.copy())}

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
    # if key == ord('c'):
    #     cv2.destroyAllWindows()
    #     cv2.imshow('Canny 2', pics["c2"])
    if key == ord('x'):
        cv2.destroyAllWindows()
        cv2.imshow('wut', cv2.Canny(img,100,200))

