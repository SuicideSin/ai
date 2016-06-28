#!/usr/local/bin/python3

#Put 100 dots on a canvas


import sys, random, cv2, time, math
import numpy as np

im = np.zeros((650,650,3), np.uint8)
im[:,:] = 0

radius = 5
lower = radius
upper = im.shape[0]-radius

flies = {}

dx = 0.1
tau = 1
const = 0.06
threshold = 0.9

def f(x):
    return 1-math.exp(-x/tau)

def df(x):
    return (1-f(x))/tau

for i in range(100):
    x, y = random.randint(lower, upper), random.randint(lower, upper)
    intensity = random.uniform(0.0, 1.0)
    flies[(x, y)] = intensity
    cv2.circle(im,(x,y), radius, (0, intensity*255, intensity*255), -1)

def update(flies):
    im = np.zeros((650,650,3), np.uint8)
    im[:,:] = 0
    
    bumps = []
    for i in flies:
        flies[i] += (1-flies[i])*dx#(f(flies[i]) + df(flies[i]) * dx)
        if flies[i] > threshold:
            flies[i] = 0.0
            bumps.append(i)
    # print(flies)
    if bumps:
        for i in flies:
            if i not in bumps:
                flies[i] += len(bumps)*const
    
    for i in flies:
        cv2.circle(im,(i[0],i[1]), radius, (0, flies[i]*255, flies[i]*255), -1)   
        
    return im



cv2.imshow('Image', im)
while True:
    key = cv2.waitKey(100)
    if key == 27:
        cv2.destroyAllWindows()
        break
    cv2.imshow('Image', update(flies))
        