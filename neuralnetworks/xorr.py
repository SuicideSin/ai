#!/usr/local/bin/python3
import sys, math, random
import numpy as np

def gradientDescent(X, Y, weights, m, alpha):
    error = 1
    step = 0
    l = len(weights)
    print("LR: {} \n10000 Steps Max\n".format(alpha))
    for step in range (10000):
        error = 0
        RMS = 0
        order = [k for k in range(m)]
        random.shuffle(order)
        for i in order:
            A = forwardProp(X[i], Y[i], weights)
            RMS += (Y[i][0].item() - A[-1][0].item())**2
            error += costFunction(A[-1], Y[i])
            gradients = calcGradients(X[i], Y[i], A, weights)
            weights[0] = weights[0] + alpha*gradients[0]
            weights[1] = weights[1] + alpha*gradients[1]
        error = error/4
        RMS = RMS/4
        if step > 2500 and RMS > 0.1:
            weights = randomInit()
            sys.stdout.write("\n")
            print("\nRestarting")
            return gradientDescent(X, Y, weights, m, alpha)
            break
        sys.stdout.write("{} \t {} \t".format(step+1, RMS) + "\n")
        sys.stdout.flush()
        if error < 0.005:
            break
    return weights

def forwardProp(x, y, weights):
    a = []
    a1 = np.insert(x, 0, 1, axis=0)
    a.append(a1)
    for i in range(len(weights) - 1):
        theta = weights[i]
        ai = sigmoid(np.transpose(theta) * a[-1])
        ai = np.insert(ai, 0, 1, axis =0)
        a.append(ai)
    an = sigmoid(np.transpose(weights[-1]) * a[-1])
    a.append(an)
    return a

def calcGradients(x, y, a, weights):
    gradients = []
    delta = []
    delta3 = y - a[-1]
    delta2 = np.multiply((weights[1]*delta3), sigmoidGradient(a[1]))
    delta2 = np.delete(delta2, 0, 0)
    
    grad1 = a[0] * np.transpose(delta2)
    gradients.append(grad1)

    grad2 = a[1] * np.transpose(delta3)
    gradients.append(grad2)
    return gradients

def costFunction(a, y):
    cost = np.sum(np.multiply(-y, np.log(a)) - np.multiply((1-y),np.log(1-a)))
    return cost

def sigmoid(z):
    return (1/(1 + np.exp(-z)))

def sigmoidGradient(g):
    return np.multiply(g, (1-g))

def randomInit():
    weights = []
    weights.append(np.matrix([[randWeight(), randWeight()] for i in range(3)]))
    weights.append(np.matrix([[randWeight()] for i in range(3)]))
    return weights

def randWeight():
    weight = random.random() * 2 -1
    return weight

def checkAnswers(X, Y, weights, m):
    for i in range(m):
        aj = forwardProp(X[i], Y[i], weights)[-1]
        print("Inputs: {} {} \t Expected: {} \tOutput: {}".format(X[i][0].item(), X[i][1].item(), Y[i][0].item(), aj[0].item()))
    print("w0: {}".format(weights[0]))
    print("w1: {}".format(weights[1]))
def main():
    ALPHA = .1
    weights = randomInit()
    X = [np.matrix([[1], [1]]), np.matrix([[1], [0]]), np.matrix([[0], [1]]), np.matrix([[0], [0]])]
    Y = [np.matrix([[0]]), np.matrix([[1]]), np.matrix([[1]]), np.matrix([[0]])]
    M = len(X)
    weights = gradientDescent(X, Y, weights, M, ALPHA)
    checkAnswers(X, Y, weights, M) 
main()