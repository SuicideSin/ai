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

def findNeighbors(t):
    i,j=t
    rowLimit = height-1
    columnLimit = width-1
    n = set()
    for x in range(max(0, i-1), min(i+1, rowLimit)+1):
        for y in range(max(0, j-1), min(j+1, columnLimit)+1):
            if x != i or y != j:
                n.add((x,y))
    return n

def bfs(graph, start, centers):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited and vertex in centers:
            visited.add(vertex)
            queue.extend(findNeighbors(vertex) - visited)
    return visited

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

hough = np.zeros((height,width,3), np.uint8)
hough[:,:] = 255

intersects = {(r, c): 0 for r in range(height) for c in range(width)}


lines = {e: set() for e in edges}
for e in edges:
    i,j = e[0], e[1]
    r,c = i,j
    
    Gx = -int(blurred[i-1,j+1][0]) + int(blurred[i+1,j+1][0]) + -2*int(blurred[i-1,j][0]) + 2*int(blurred[i+1,j][0]) + -int(blurred[i-1,j-1][0]) + int(blurred[i+1,j-1][0])
    Gy = int(blurred[i-1,j+1][0]) + 2*int(blurred[i,j+1][0]) + int(blurred[i+1,j+1][0]) + -int(blurred[i-1,j-1][0]) + -2*int(blurred[i,j-1][0]) + -int(blurred[i+1,j-1][0])
    
    angle = math.atan2(Gy, Gx)# * 180 / math.pi
    
    slope = -math.tan(angle+math.pi/2)

    while 0 < c < width and 0 < r < height:
        hough[int(r),c] -= 1
        intersects[(int(r), c)] += 1
        lines[e].add((c,r))
        c+=1
        r+=slope
    r,c = i,j
    while 0 < c < width and 0 < r < height:
        hough[int(r),c] -= 1
        intersects[(int(r), c)] += 1
        lines[e].add((c,r))
        c-=1
        r-=slope

centers = set()
for r in range(1, height-1):
    for c in range(1, width-1):
        val = (intersects[r-1,c+1] +
               intersects[r  ,c+1] +
               intersects[r+1,c+1] +
               intersects[r-1,c  ] +
               intersects[r  ,c  ] +
               intersects[r+1,c  ] +
               intersects[r-1,c-1] +
               intersects[r  ,c-1] +
               intersects[r+1,c-1]) / 9
        
        T = int(sys.argv[4]) if len(sys.argv) > 4 else 70
        if val > T:
            centers.add((r,c))

clusters = set()
visited = set()
for i in centers:
    if i not in visited:
        cluster = bfs(hough, i, centers)
        clusters.add(frozenset(cluster))
        visited |= cluster

print("Centers: {}".format(len(clusters)))

centers = set()
circles = img.copy()

white = np.zeros((height,width,3), np.uint8)
white[:,:] = 255
white = canny.copy()

for cluster in clusters:
    radii = {}
    
    r = [i[0] for i in cluster]
    c = [i[1] for i in cluster]
    cr = int(sum(r)/len(r))
    cc = int(sum(c)/len(c))
    cv2.circle(circles,(cc,cr), 1, (0,255,0), -1)
    cv2.circle(white,(cc,cr), 1, (0,255,0), -1)
    centers.add((cr,cc))
    for edge in lines:
        if cluster.isdisjoint(lines[edge]):
            radius = int(math.sqrt((edge[0]-cr)**2 +(edge[1]-cc)**2))
            if radius in radii:
                radii[radius] += 1
            else:
                radii[radius] = 1
    radii = {r: radii[r]/r for r in radii if r != 0}
    
    rad = max(radii, key=radii.get)
    radT = float(sys.argv[5]) if len(sys.argv) > 5 else 1.5
    while radii[rad] > radT: #Best value so far would be 1.5
        cv2.circle(circles,(cc,cr),rad, (0,255,0), 1)
        cv2.circle(white,(cc,cr), rad, (0,255,0), 1)
        for i in range(5):
            if rad+i in radii:
                del radii[rad+i]
            if rad-i in radii:
                del radii[rad-i]
        if not radii:
            break
        rad = max(radii, key=radii.get)

cv2.imshow('Circles', circles)
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
    if key == ord('c'):
        cv2.destroyAllWindows()
        cv2.imshow('Circles', circles)
    if key == ord('w'):
        cv2.destroyAllWindows()
        cv2.imshow('Circles', white)