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

4132 -> 1432 3142 2134 | 4312 4231 | 4123

51243 -> 15243 21543 41253 31245 | 52143 54213 53241 | 51423 51234 | 51342 

A. Investigate how long it takes to solve the n-queens problem 
    1. If you only make a swap when it improves your position
        a. Graph the number of swaps till you find a solution against n 
    
        2. Also graph the number of shuffles

        3. What is the percent of times that there is a lateral swap possibility just prior              to a shuffle (as a function of n)? A lateral swap is a swap that makes the number             of conflicts stay the same

B. Implement a lateral shuffle approach that improves on A
    1. graph against n
    
    
    
    
38 cities 
Read in each city from file, make a dictionary
create list
e.g. [1, 12, 27, ... 6, 32, 25]
find total distance traveled


ASSIGNMENTS:


'''
