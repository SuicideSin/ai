#!/usr/local/bin/python3
import math, random, time, sys, os
cols = int(os.popen('stty size', 'r').read().split()[1])

def dist(t1, t2): return math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2)

def cost(path, n): return sum([dist(cities[path[i]], cities[path[i+1]]) for i in range(-1, n-1)])

def allSwaps(path, n): return {i for i in {tuple(path[:i] + [path[j]] + path[i+1:j] + [path[i]] + path[j+1:]) for i in range(n) for j in range(n)} if len(i) == n}

def hillClimb(path, n):
    visited = set()
    c, p = cost(path, n), float("inf")
    while c < p:
        costDict = {i: cost(i, n) for i in allSwaps(path, n) if i not in visited}
        path = list(min(costDict, key=costDict.get))
        p, c = c, cost(path, n)
    return path
    
def greedy(n, path):
    dists = {i: dist(cities[path[-1]], cities[i]) for i in range(1,n+1) if i not in path and i != path[-1]}
    if dists:
        path.append(min(dists, key=dists.get))
        greedy(n, path)
    return path    

def greedier(n, path, t):
    dists = {i: cost(i, n) for i in {tuple(greedy(n, [random.randint(1, n)])) for j in range(t)}}
    return min(dists, key=dists.get)

def results(func, name, args):
    tick = time.clock()
    s = func(*args)
    tock = time.clock()
    print("{}\n\033[1;32m{}\033[0m:\n{}\nTotal distance: {}\nFound in {} seconds.".format("-"*cols, name, s, cost(s, n), tock-tick))
    return s

numCities = 38 if len(sys.argv) > 1 and sys.argv[1] == '38' else 734 if len(sys.argv) > 1 and sys.argv[1] == '734' else 38

cities = {i: j for (i, j) in enumerate((tuple([float(i) for i in line.rstrip('\n').split()])) for line in open('{}cities.txt'.format(numCities), 'r')) if len(j) > 1}

n = len(cities)
path = random.sample([i for i in range(1, n+1)], n)

print("\033[1;32mRandom Path\033[0m:")
print(path)
print("Total distance: {}".format(cost(path, n)))
# Hill climbing
if numCities == 38:
    hc = results(hillClimb, "Local Min using swapping", (path, n))
# Greedy
g = results(greedier, "Greedy Algorithm", (n, [random.randint(1, n)], 10))