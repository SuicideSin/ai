#!/usr/local/bin/python3
import time, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
 
def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
 
def solve(n):
    solutions = [[]]
    for row in range(n):
        solutions = (solution+[i+1]
                       for solution in solutions # first for clause is evaluated immediately,
                                                 # so "solutions" is correctly captured
                       for i in range(n)
                       if not under_attack(i+1, solution))
    return solutions

start = time.clock()
answers = solve(n)
count = 0
for i in answers:
    #print(list(enumerate(i, start=1)))
    count += 1
end = time.clock()
# first_answer = next(answers)
# print(list(enumerate(first_answer, start=1)))
print("{} solutions in {} sec.".format(count, end-start))