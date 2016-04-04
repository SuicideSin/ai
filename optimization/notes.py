'''
N Queens Problem
How many queens can exist on an N by N board without being able to attack eachother?
Given an N, give the number of distinct solutions and determine the exact solutions

A solution can be represented by a string permutation.

"123456" represents queens located along the diagonal

By definition, all rows and all cols must contain 1 queen in an N-queens solution

'''


'''
1. Write a function that takes an n-queens position and returns the number of conflicts there are <- make this efficient

Optimization strategies:
    - Hill climbing:
        - Finding local maxima/minima

2. Given a command line input, n, find a solution to the n-queens problem by taking an arbitrary permutation string and using hill climbing where you check all possible swaps for improvement (Print out permutation string and board)

n*(n-1)/2
'''
