import cv2, sys, re, math, urllib.request
import numpy as np

# Default image file
imgSpec = "duck.jpg"
if len(sys.argv) > 1: imgSpec = sys.argv[1]


# Decide between file & url with regular expression (re)
if re.compile("^\\w*\\:\\/\\/").search(imgSpec) is None:
  im = cv2.imread(imgSpec, cv2.IMREAD_COLOR)
else:
  resp = urllib.request.urlopen(imgSpec)
  im = np.asarray(bytearray(resp.read()), dtype = "uint8")
  im = cv2.imdecode(im, cv2.IMREAD_COLOR)


# Allows window to be resized by user (in theory)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
height, width = im.shape[:2]    # Get image dimensions
widthMax = 1024                  # The screen width, in pixels
if (width > widthMax):
  cv2.resizeWindow('image', widthMax, int(height*widthMax/width))

height, width, depth = im.shape

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,150,200,apertureSize = 3)

cv2.imshow('houghlines',im)

while(True):
    img = im.copy()
    k = cv2.waitKey(0)

    if k == ord('h'):   # Press 'h' to enable cv2.HoughLines()
        lines = cv2.HoughLines(edges,1,np.pi/180,275)
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))   # Here i have used int() instead of rounding the decimal value, so 3.8 --> 3
            y1 = int(y0 + 1000*(a))    # But if you want to round the number, then use np.around() function, then 3.8 --> 4.0
            x2 = int(x0 - 1000*(-b))   # But we need integers, so use int() function after that, ie int(np.around(x))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow('houghlines',img)

    elif k == ord('p'): # Press 'p' to enable cv2.HoughLinesP()
        lines = cv2.HoughLinesP(edges,1,np.pi/180,150, minLineLength = 100, maxLineGap = 10)
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow('houghlines',img)

    elif k == 27:    # Press 'ESC' to exit
        break

cv2.destroyAllWindows()