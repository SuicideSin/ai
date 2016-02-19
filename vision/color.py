#!/usr/local/bin/python3
import numpy as np
import urllib
import cv2
import sys
 
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = 'polarbear.jpg'

img = cv2.imread(fname, -1)

cv2.imshow(fname[0:fname.find('.')], img)

while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        break
