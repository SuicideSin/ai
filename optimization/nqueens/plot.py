#!/usr/local/bin/python3
import sys, time, random
n = 8
def conflicts(queens, n): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)])

def display(queens, n): print ("\n".join('| ' + '. ' * (int(i)-1) + '\033[1;32mX\033[0m ' + '. ' * (n-int(i)) + '|' for i in queens) + "\n" + " " + "-"*(2*n+1) + " ")

def allSwaps(queens, n): return {i for i in {tuple(queens[:i] + [queens[j]] + queens[i+1:j] + [queens[i]] + queens[j+1:]) for i in range(n) for j in range(n)} if len(i) == n}

def hillClimb(queens, n):
    swaps, shuffles, laterals, total = 0, 0, 0, 0
    visited = set()
    c = conflicts(queens, n)
    while c > 0:
        conflictDict = {i: conflicts(i, n) for i in allSwaps(queens, n) if i not in visited}
        swaps += len(conflictDict)
        minConflict = min(conflictDict, key=conflictDict.get)
        if conflictDict[minConflict] < c:
            queens = list(minConflict)
        else:
            if minConflict not in visited:
                laterals += 1
            queens = random.sample(queens, n)
            shuffles += 1
        visited.add(minConflict)
        c = conflicts(queens, n)
        total += 1
    return (queens, swaps, shuffles, laterals, total)

sw = open('plot/swaps.txt', 'w+')
sh = open('plot/shuffles.txt', 'w+')
lat = open('plot/laterals.txt', 'w+')

t = 100

for n in range(4, 51):
    totalSwaps = 0
    totalShuffles = 0
    totalLaterals = 0
    totalTotal = 0
    start = time.clock()
    for i in range(t):
        queens = random.sample(range(1, n+1), n)
        soln, swaps, shuffles, laterals, total = hillClimb(queens, n)
        totalSwaps += swaps
        totalShuffles += shuffles
        totalLaterals += laterals
        totalTotal += total
    end = time.clock()
    sw.write("{}\t{}\n".format(n, totalSwaps/t))
    sh.write("{}\t{}\n".format(n, totalShuffles/t))
    lat.write("{}\t{}\n".format(n, totalLaterals/totalTotal*100))
    #print(soln)
    print("{} trials of {} by {} finished in {} seconds.".format(t, n, n,  end-start))
    print("{} swaps,\t{} shuffles,\t{}% laterals".format(totalSwaps/t, totalShuffles/t, totalLaterals/totalTotal*100))