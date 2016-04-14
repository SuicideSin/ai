#!/usr/local/bin/python3
import sys, time, random, itertools
from itertools import permutations

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
queens = sys.argv[2] if len(sys.argv) > 2 else random.sample([i for i in range(1, n+1)], n)

def conflicts(queens): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)])

def display(queens): print ("\n".join('| ' + '. ' * (int(i)-1) + '\033[1;32mX\033[0m ' + '. ' * (n-int(i)) + '|' for i in queens) + "\n" + " " + "-"*(2*n+1) + " ")

def solve(queens):
    perms = {p for p in permutations(''.join(str(i) for i in range(1, n+1)))}
    for perm in perms:
        if conflicts(perm) == 0:
            return perm

def allSwaps(queens):
    swaps = [list(i) for i in {tuple(queens[:i] + [queens[j]] + queens[i+1:j] + [queens[i]] + queens[j+1:]) for i in range(n) for j in range(n)} if len(i) == n]
    #swaps = [list(i) for i in swaps if len(i) == n]
    #list(swaps for swaps,_ in itertools.groupby(swaps))
    #assert len(swaps) == n*(n-1)/2
    return swaps

def hillClimb(queens):
    while conflicts(queens) > 0:
        conflictDict = {tuple(i): conflicts(i) for i in allSwaps(queens)}
        minConflict = min(conflictDict, key=conflictDict.get)
        queens = list(minConflict) if conflictDict[minConflict] < conflicts(queens) else random.sample(queens, n)
    return queens

def solveAll(queens):
    perms = {p for p in permutations(''.join(str(i) for i in range(1, n+1)))}
    return {perm for perm in perms if conflicts(perm) == 0}
    
start = time.clock()
#solns = solveAll(queens)
#soln = solve(queens)
soln = hillClimb(queens)
end = time.clock()
# for soln in solns: display(soln)
# print("{} Solutions found for a {} by {} board in {} seconds.".format(len(solns), n, n,  end-start))
print(soln)
display(soln)
print("Solution found for a {} by {} board in {} seconds.".format(n, n,  end-start))