#!/usr/local/bin/python3
import numpy as np
import math, sys, random

mode = sys.argv[1].lower() if len(sys.argv) > 1 else "and"

if mode == "not":               #NOT
    print("not")
    training = {0: 1,
                1: 0}
elif mode == "or":              #OR
    print("or")
    training = {(0, 0): 0,
                (1, 0): 1,
                (0, 1): 1,
                (1, 1): 1}
else:                           #AND
    print("AND")
    training = {(0, 0): 0,
                (1, 0): 0,
                (0, 1): 0,
                (1, 1): 1}

single = ["not"]
inputs = 1 if mode in single else len(list(training.keys())[0])
b, w = 0, tuple(0 for i in range(inputs)) #bias, weights
e = math.e

def neuron(x, w, b): #sigmoid function. returns: float
    return 1/(1+math.exp(-(np.dot(w, x)+b)))

def maxError(w, b): #safety check. returns: float
    return max([v - neuron(k, w, b) for k,v in training.items()])

def mse(w, b): #minimize this. returns: float
    return 1/len(training)*sum([a - neuron(x, w, b) for x,a in training.items()])**2

def vary(w, b): #random mutations to weights and biases. returns: ((wx, wy), b)
    return tuple(tuple([tuple(weight+random.uniform(-5, 5) for weight in w), b+random.uniform(-5, 5)]) for i in range(2))

def optimize(w, b):
    while maxError(w, b) > 0.1:
        w,b=tuple(random.uniform(-0.5, 0.5) for i in range(inputs)), random.uniform(-0.5, 0.5)
        while mse(w, b) > 10**-15:
            error = {i: mse(*i) for i in vary(w, b)}
            w, b = min(error, key=error.get)
    return (w, b)

def results(w, b):
    print("w: {}".format(w))
    print("b: {}".format(b))
    for i in training.keys():
        print("{}: {}".format(i, (neuron(i, w, b))))
    print("MSE: {}\n".format(mse(w, b)))
    
results(w, b)
results(*optimize(w, b))