#!/usr/local/bin/python3
import numpy as np
import urllib
import cv2
import sys
import time
 
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = 'polarbear.jpg'
    

img = cv2.imread(fname, -1)
    
height, width, depth = img.shape

grayscale = np.array([0.3, 0.59, 0.11])

gauss = np.array([[1, 2, 1],
                  [2, 4, 2],
                  [1, 2, 1]])/16

tick = time.clock()
for i in range(height):
    for j in range(width):
        img[i, j] = np.dot(grayscale, img[i, j])
print("Time: {}".format(time.clock()-tick))



cv2.imshow(fname[0:fname.find('.')], img)

cv2.waitKey(0)
cv2.destroyAllWindows()
