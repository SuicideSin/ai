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

tick = time.clock()
for i in range(height):
    for j in range(width):
        img[i, j] = np.dot(grayscale, img[i, j])
print("Time: {}".format(time.clock()-tick))

blurred = cv2.filter2D(img, -1, gauss)

#edges = cv2.Canny(blurred,100,200)

cv2.imshow('Guassian Blur', blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
 


# plt.subplot(121),plt.imshow(img),plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(blurred),plt.title('Blurred')
# plt.xticks([]), plt.yticks([])
# plt.show()
