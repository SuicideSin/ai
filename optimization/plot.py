#!/usr/local/bin/python3
import sys, time, random
n = 4
def conflicts(queens, n): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)])

def display(queens, n): print ("\n".join('| ' + '. ' * (int(i)-1) + '\033[1;32mX\033[0m ' + '. ' * (n-int(i)) + '|' for i in queens) + "\n" + " " + "-"*(2*n+1) + " ")

def allSwaps(queens, n): return [list(i) for i in {tuple(queens[:i] + [queens[j]] + queens[i+1:j] + [queens[i]] + queens[j+1:]) for i in range(n) for j in range(n)} if len(i) == n]

def hillClimb(queens, n):
    swaps = 0
    shuffles = 0
    while conflicts(queens, n) > 0:
        conflictDict = {tuple(i): conflicts(i, n) for i in allSwaps(queens, n)}
        #assert len(conflictDict) == n*(n-1)/2
        minConflict = min(conflictDict, key=conflictDict.get)
        if conflictDict[minConflict] < conflicts(queens, n):
            queens = list(minConflict)
            swaps += 1
        else:
            queens = random.sample(queens, n)
            shuffles += 1
    return (queens, swaps, shuffles)

sw = open('swaps.txt', 'w+')
sh = open('shuffles.txt', 'w+')

t = 100

for n in range(4, 51):
    totalSwaps = 0
    totalShuffles = 0
    start = time.clock()
    for i in range(t):
        queens = random.sample(range(1, n+1), n)
        soln, swaps, shuffles = hillClimb(queens, n)
        totalSwaps += swaps
        totalShuffles += shuffles
    end = time.clock()
    sw.write("{}\t{}\n".format(n, swaps/t))
    sh.write("{}\t{}\n".format(n, shuffles/t))
    #print(soln)
    print("{} trials of {} by {} finished in {} seconds.".format(t, n, n,  end-start))