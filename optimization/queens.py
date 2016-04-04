#!/usr/local/bin/python3
import sys, time, random
from itertools import permutations

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8

perms = {''.join(p) for p in permutations(''.join(str(i) for i in range(1, n+1)))}
queens = sys.argv[2] if len(sys.argv) > 2 else perms.pop()

def conflicts(queens):
    return len([1 for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(int(queens[i-1])-int(queens[j-1])) == abs(i-j)])

def display(queens):
    print ("\n".join('. ' * (int(i)-1) + '\033[1;32mX\033[0m ' + '. ' * (n-int(i)) for i in queens) + "\n" + "-"*(2*n-1) + "\n")

def solve(queens, perms):
    perm = queens
    while conflicts(perm) > 0:
        perm = perms.pop()
    return perm

def solveAll(queens, perms):
    s = set()
    perm = queens
    while perms:
        if conflicts(perm) == 0:
            s.add(perm)
        perm = perms.pop()
    return s
    
# print(queens)
# display(queens)
start = time.clock()
solns = solveAll(queens, perms)
end = time.clock()
for soln in solns:
    display(soln)
print("{} Solutions found in {} seconds.".format(len(solns), end-start))