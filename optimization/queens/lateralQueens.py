#!/usr/local/bin/python3
import sys, time, random

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
queens = [int(sys.argv[i]) for i in range(2, n+2)] if len(sys.argv) == n+2 else [int(i) for i in sys.argv[2]] if len(sys.argv) == 3 and n < 10 else random.sample(range(1, n+1), n)

def conflicts(queens, n): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)])

def display(queens, n): print ("\n".join('| ' + '. ' * (i-1) + '\033[1;32mX\033[0m ' + '. ' * (n-i) + '|' for i in queens) + "\n" + " " + "-"*(2*n+1) + " ")

def allSwaps(queens, n): return {i for i in {tuple(queens[:i] + [queens[j]] + queens[i+1:j] + [queens[i]] + queens[j+1:]) for i in range(n) for j in range(n)} if len(i) == n}

def hillClimb(queens, n):
    visited = set()
    c = conflicts(queens, n)
    while c > 0:
        conflictDict = {i: conflicts(i, n) for i in allSwaps(queens, n) if i not in visited}
        minConflict = min(conflictDict, key=conflictDict.get)
        queens = list(minConflict) if conflictDict[minConflict] < c or (conflictDict[minConflict] == c and minConflict not in visited) else random.sample(queens, n)
        visited.add(minConflict)
        c = conflicts(queens, n)
    return queens

start = time.clock()
soln = hillClimb(queens, n)
end = time.clock()
print(queens)
display(queens, n)
print(soln)
display(soln, n)
print("Solution found for a {} by {} board in {} seconds.".format(n, n,  end-start))