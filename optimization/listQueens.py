#!/usr/local/bin/python3
import sys, time, random

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
queens = [int(sys.argv[i]) for i in range(2, n+2)] if len(sys.argv) == n+2 else [int(i) for i in sys.argv[2]] if len(sys.argv) == 3 and n < 10 else random.sample([i for i in range(1, n+1)], n)

def conflicts(queens): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)])

def display(queens): print ("\n".join('| ' + '. ' * (int(i)-1) + '\033[1;32mX\033[0m ' + '. ' * (n-int(i)) + '|' for i in queens) + "\n" + " " + "-"*(2*n+1) + " ")

def allSwaps(queens):
    return [list(i) for i in {tuple(queens[:i] + [queens[j]] + queens[i+1:j] + [queens[i]] + queens[j+1:]) for i in range(n) for j in range(n)} if len(i) == n]

def hillClimb(queens):
    while conflicts(queens) > 0:
        conflictDict = {tuple(i): conflicts(i) for i in allSwaps(queens)}
        #assert len(conflictDict) == n*(n-1)/2
        minConflict = min(conflictDict, key=conflictDict.get)
        queens = list(minConflict) if conflictDict[minConflict] < conflicts(queens) else random.sample(queens, n)
    return queens
    
start = time.clock()
soln = hillClimb(queens)
end = time.clock()
print(queens)
display(queens)
print(soln)
display(soln)
print("Solution found for a {} by {} board in {} seconds.".format(n, n,  end-start))