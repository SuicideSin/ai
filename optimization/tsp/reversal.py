#!/usr/local/bin/pypy3
import math, random, time, sys, os
cols = int(os.popen('stty size', 'r').read().split()[1])

def dist(t1, t2): return math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2)

# def cost(path, n): return sum([dist(cities[path[i]], cities[path[i+1]]) for i in range(-1, n-1)])
#
def linCost(path,n): return sum([cityCosts[path[i]][path[i+1]] for i in range(0, n-1)])

def allReversals(path, n): return {i:j for i,j in {tuple(path[:i] + path[i:j+1][::-1] + path[j+1:]): (i,j) for i in range(n) for j in range(n)}.items() if len(i) == n}
#MAKE SURE THIS WORKS FOR WHEN i < j

def cost(path, n): return sum([cityCosts[path[i]][path[i+1]] for i in range(-1, n-1)])

def hillClimb(path, n):
    visited = set()
    c, p = cost(path, n), float("inf")
    while c < p:
        costDict = {i: (c-linCost(path[a:b+1], len(path[a:b+1]))+linCost(i[a:b+1], len(i[a:b+1])), (a,b)) for i, (a,b) in allReversals(path, n).items() if i not in visited}
        minEl = list(min(costDict.items(), key=lambda x: x[1][0]))
        path, (a, b) = list(minEl[0]), minEl[1][1]
        sub = path[a:b+1]
        subLen = len(sub)
        p, c = c, (c-linCost(sub[::-1], subLen)+linCost(sub, subLen))
        #print(path)
        visited.add(tuple(path))
    return path
    
def greedy(path, n):
    dists = {i: dist(cities[path[-1]], cities[i]) for i in range(1,n+1) if i not in path and i != path[-1]}
    if dists:
        path.append(min(dists, key=dists.get))
        greedy(path, n)
    return path    

def greedier(path, n, t):
    dists = {i: cost(i, n) for i in {tuple(greedy([random.randint(1, n)], n)) for j in range(t)}}
    return min(dists, key=dists.get)
    
def greedyReversal(path, n):
    return hillClimb(form(greedier(path, n, 10), n), n)

def results(n, func, name, args):
    tick = time.clock()
    s = form(func(*args), n)
    assert len(s) == len(set(s))
    tock = time.clock()
    print("{}\n\033[1;32m{}\033[0m:\n{}\nTotal distance: {}\nFound in {} seconds.".format("-"*cols, name, s, cost(s, n), tock-tick))
    return s

def form(path, n):
    i = path.index(1)
    path = list(path[i:] + path[:i])
    if path[1] > path [-1]:
        path = [path[0]] + [path[i] for i in range(n-1, 0, -1)]
    return path

numCities = 38 if len(sys.argv) > 1 and sys.argv[1] == '38' else 734 if len(sys.argv) > 1 and sys.argv[1] == '734' else 38

cities = {i: j for (i, j) in enumerate((tuple([float(i) for i in line.rstrip('\n').split()])) for line in open('{}cities.txt'.format(numCities), 'r')) if len(j) > 1}

cityCosts = {i: {j: dist(cities[i], cities[j]) for j in cities if j != i} for i in cities}

n = len(cities)
path = random.sample([i for i in range(1, n+1)], n)

print("\033[1;32mRandom Path\033[0m:")
print(path)
print("Total distance: {}".format(cost(path, n)))

# Hill climbing

hc = results(n, greedyReversal, "Greedy + Local Min using reversals", (path, n))
f = open('reversaldata.txt', 'w+')
for i in hc:
    f.write("{}\t{}\n".format(round(cities[i][0]), (cities[i][1])))
f.write("{}\t{}\n".format(round(cities[1][0]), (cities[1][1])))