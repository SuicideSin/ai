#!/usr/local/bin/python3
import sys, time, itertools, random

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8

queens = set()
allPos = [(r,c) for r in range(n) for c in range(n)]
solutions = []

def transpose(queens):
    return [{(abs(j-n+1), i) for (i, j) in queens}, {(j, abs(i-n+1)) for (i, j) in queens}, {(abs(i-n+1), abs(j-n+1)) for (i, j) in queens}, {(abs(i-n+1), j) for (i, j) in queens}, {(i, abs(j-n+1)) for (i, j) in queens}, {(abs(j-n+1), abs(i-n+1)) for (i, j) in queens}, {(j, i) for (i, j) in queens}]

def findPossible(queens):
    possible = set(allPos)
    for queen in queens:
        for pos in allPos:
            if pos[0] == queen[0] or pos[1] == queen[1] or abs(pos[0]-queen[0]) == abs(pos[1]-queen[1]):
                possible -= {pos}
    return possible
    
def board(queens):
    print ("\n".join(["".join('\033[1;32mX\033[0m ' if (i, j) in queens else ". " for j in range(n)) for i in range(n)]) + "\n" + "-"*(2*n-1))
    print(queens)
    
def solve(queens, visited=None):
    if visited is None:
        visited = []
    if len(queens) == n and queens not in solutions:
        solutions.append(queens)
        return
    visited.append(queens)
    for pos in findPossible(queens):
        tmp = queens | {pos}
        if tmp not in visited:
            solve(tmp)
    return visited

tick = time.clock()
solve(queens)
tock = time.clock()
unique = solutions.copy()
for i in solutions:
    board(i)
    for j in solutions:
        if any([k == j for k in transpose(i)]):
            if i in unique:
                unique.remove(i)
                
print("\n{} solutions found in {} seconds.".format(len(solutions), tock-tick))
print("{} unique solutions.".format(len(unique)))