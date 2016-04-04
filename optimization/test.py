#!/usr/local/bin/python3
import time, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
 
def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
 
def solve(n):
    solutions = [[]]
    for row in range(n):
        # for i in range(n):
        #     for solution in solutions:
        #         if not under_attack(i, solution):
        #             solution + [i]
        #             solutions.append(solution+[i])
        solutions = [solution+[i]
                       for solution in solutions
                       for i in range(n)
                       if not under_attack(i, solution)]
    return solutions

def printSolutions(solutions):
    for i in range(2*n-1): print('-',end="")
    print()
    for solution in solutions:
        for i in range(n):
            for j in range(n):
                print("{} ".format('\033[1;32mX\033[0m' if (i, j) in solution else '.'),end="")
            print()
        for i in range(2*n-1): print('-',end="")
        print()

start = time.clock()
solutions = solve(n)
end = time.clock()
final = []
for answer in solutions: 
    print(set(enumerate(answer)))
    final.append(set(enumerate(answer)))
    
printSolutions(final)
    
print("{} sec.".format(end-start))
print(len(solutions))