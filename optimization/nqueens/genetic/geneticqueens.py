#!/usr/local/bin/python3
import sys, time, random, operator, heapq, bisect
from numpy.random import choice

mutateProb = 5

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
queens = [int(sys.argv[i]) for i in range(2, n+2)] if len(sys.argv) == n+2 else [int(i) for i in sys.argv[2]] if len(sys.argv) == 3 and n < 10 else random.sample(range(1, n+1), n)

def conflicts(queens): return len([True for i in range(1, n+1) for j in range(1, n+1) if i != j and abs(queens[i-1]-queens[j-1]) == abs(i-j)]) + (len(queens) - len(set(queens)))

# def printf(queens):
#     print ("\n".join([ "[" + ", ".join(str(i) for i in queens[i:i+10]) + "]" for i in range(0, n, 10) ]))

def mutate(queens):
    queens = list(queens)
    l = [random.randint(0,n-1), random.randint(0,n-1)]
    p1 = min(l)
    p2 = max(l)
    return queens[:p1] + [queens[p2]] + queens[p1+1:p2] + [queens[p1]] + queens[p2+1:]

def reproduce(mom, dad):
    pivot = random.randint(1,n-1)
    c1 = mom[:pivot]+dad[pivot:]
    c2 = dad[:pivot]+mom[pivot:]
    if random.randint(0, 100) == mutateProb:
        return [tuple(mutate(c1)), tuple(mutate(c2))]
    return [i for i in [c1, c2] if len(set(i)) == len(i)]

def genetic(n):
    start = 500
    pool = set()
    while len(pool) < start:
        pool.add(tuple(random.sample(range(1, n+1), n)))
    epoch = 0
    while True:
        print(len(pool))
        fit = {i: conflicts(i) for i in pool}
        fitList = list(fit.items())
        #boards, fitness = zip(*fitList)
        #average = sum(fitness)/len(fitness)

        best = min(fitList, key = lambda t: t[1])
        print("{}:\t{}".format(epoch, best[1]))
        if best[1] == 0: return best[0]
        
        
        for i in heapq.nlargest(len(fitList)-start, fitList, key = lambda t: t[1]):
            fitList.remove(i)
            pool.remove(i[0])

        # for i in range(len(fitList)):
        #     if fitness[i] > average:
        #         fitList.remove((boards[i], fitness[i]))
        #         pool.remove(boards[i])

        # keys, values = zip(*fitList)
        # pSum = sum(values)
        # pList = [v/pSum for v in values]
        #print((pList))
        for i in range(0, len(fitList)):
            for j in reproduce(fitList[random.randint(0,len(fitList)-1)][0], fitList[random.randint(0,len(fitList) - 1)][0]):
            #p1, p2 = choice(range(len(fitList)), 2, p=pList)
            #for j in reproduce(fitList[p1][0], fitList[p2][0]):
                if len(j) == n:
                    pool.add(j)
        epoch += 1

start = time.clock()
soln = genetic(n)
stop = time.clock()

#printf(soln[0])
print(soln)
print("Solution found in {} seconds.".format(stop-start))

