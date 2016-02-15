#!/usr/local/bin/python3
import numpy as np
import cv2, sys, re
import urllib.request


# Default image file
imgSpec = "http://ramsau.com/blog/" + \
          "wp-content/uploads/Klettersteig_Skywalk.jpg"
if len(sys.argv) > 1: imgSpec = sys.argv[1]


# Decide between file & url with regular expression (re)
if re.compile("^\\w*\\:\\/\\/").search(imgSpec) is None:
  img = cv2.imread(imgSpec, cv2.IMREAD_COLOR)
else:
  resp = urllib.request.urlopen(imgSpec)
  img = np.asarray(bytearray(resp.read()), dtype = "uint8")
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)


# Allows window to be resized by user (in theory)
cv2.namedWindow('imgWnd', cv2.WINDOW_NORMAL)
height, width = img.shape[:2]    # Get image dimensions
widthMax = 1024                  # The screen width, in pixels
if (width > widthMax):
  cv2.resizeWindow('imgWnd', widthMax, int(height*widthMax/width))


# Now show the image
cv2.imshow('imgWnd',img)


# More code needed here to keep imgWnd around
cv2.waitKey(0)
cv2.destroyAllWindows()