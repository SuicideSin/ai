#!/usr/local/bin/python3
import numpy as np
import math, random

training = np.array([
    (np.array([0, 0]), 0),
    (np.array([0, 1]), 1),
    (np.array([1, 0]), 1),
    (np.array([1, 1]), 0)
])

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))
    
def deriv(z):
    return sigmoid(z)*(1-sigmoid(z))

def feedForward(x):
    for w, b in zip(weights, biases):
        x = sigmoid(np.dot(w, x)+b)
    return x

def update(data, lr):
    global weights, biases
    nb = [np.zeros(b.shape) for b in biases]
    nw = [np.zeros(w.shape) for w in weights]
    for x, y in data:
        dnb, dnw = backprop(x, y)
        nb = [nb+dnb for nb, dnb in zip(nb, dnb)]
        nw = [nw+dnw for nw, dnw in zip(nw, dnw)]
    weights = [w-(lr/len(data))*nw for w, nw in zip(weights, nw)]
    biases = [b-(lr/len(data))*nb for b, nb in zip(biases, nb)]
    
def backprop(x, y):
    global weights, biases
    nabla_b = [np.zeros(b.shape) for b in biases]
    nabla_w = [np.zeros(w.shape) for w in weights]
    # feedforward
    activation = x
    activations = [x] # list to store all the activations, layer by layer
    zs = [] # list to store all the z vectors, layer by layer
    for b, w in zip(biases, weights):
        print("{}; {}".format(w, activation))
        z = np.dot(w, activation)+b
        zs.append(z)
        activation = sigmoid(z)
        activations.append(activation)
    # backward pass
    delta = cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
    nabla_b[-1] = delta
    nabla_w[-1] = np.dot(delta, activations[-2].transpose())
    for l in range(2, layers):
        z = zs[-l]
        sp = sigmoid_prime(z)
        delta = np.dot(weights[-l+1].transpose(), delta) * sp
        nabla_b[-l] = delta
        nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
    return (nabla_b, nabla_w)
    
def descend(data, trials, mini_batch_size, lr,
        test_data=None):
    if test_data: n_test = len(test_data)
    n = len(data)
    for j in range(trials):
        random.shuffle(data)
        mini_batches = [data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
        for mini_batch in mini_batches:
            update(mini_batch, lr)
        if test_data:
            print("Trial {}: {} / {}".format(j, evaluate(test_data), n_test))
        else:
            print("Trial {} complete".format(j))

def evaluate(data):
    results = [(np.argmax(self.feedforward(x)), y) for (x, y) in data]
    return sum(int(x == y) for (x, y) in results)

def cost_derivative(output_activations, y):
    return (output_activations-y)

layers = 3
trials = 40000
dims = [3, 2, 1]
biases = [np.random.randn(i, 1) for i in dims[1:]]
weights = [np.random.randn(i, j) for i, j in zip(dims[:-1], dims[1:])]

descend(training, 30, 4, 3.0)

#for i in range(trials): #around 40000
    # for j in range(len(trainingArr)):
#         # forward-pass of a 3-layer neural network:
#         h1 = sigmoid(np.dot(W1, x) + b1) # calculate first hidden layer activations (4x1)
#         h2 = sigmoid(np.dot(W2, h1) + b2) # calculate second hidden layer activations (4x1)
#         out = np.dot(W3, h2) + b3 # output neuron (1x1)
#    res = feedForward(x)
    
    
'''
1. Calculate FeedForward(trainingArr[j], weightsArr)
    weightsArr = [[......], [..], [.]] where each "." represents a weight in a layer
    nodesArr = [[0, 1, 1]]
    def squashMe(x):
        return 1/(1+exp(-x))
2. Calculate Gradient
3. Update weights
'''