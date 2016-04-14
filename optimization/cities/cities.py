#!/usr/local/bin/python3
import math, random, time, sys

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

def greedier(n, path):
    dists = {i: cost(i, n) for i in {tuple(greedy(n, [random.randint(1, n)])) for j in range(5)}}
    return min(dists, key=dists.get)

numCities = 38 if len(sys.argv) > 1 and sys.argv[1] == '38' else 734 if len(sys.argv) > 1 and sys.argv[1] == '734' else 38

cities = {i: j for (i, j) in enumerate((tuple([float(i) for i in line.rstrip('\n').split()])) for line in open('{}cities.txt'.format(numCities), 'r')) if len(j) > 1}

n = len(cities)
path = random.sample([i for i in range(1, n+1)], n)

print("\033[1;32mRandom Path\033[0m:")
print(path)
print("Total distance: {}".format(cost(path, n)))
print("-"*80)
#
print("\033[1;32mLocal Min using swapping\033[0m:")
start = time.clock()
s = hillClimb(path, n)
end = time.clock()
print(s)
print("Total distance: {}".format(cost(s, n)))
print("Found in {} seconds.".format(end-start))
print("-"*80)
#
print("\033[1;32mGreedy Algorithm\033[0m:")
start = time.clock()
s2 = greedier(n, [random.randint(1, n)])
end = time.clock()
print(s2)
print("Total distance: {}".format(cost(s2, n)))
print("Found in {} seconds.".format(end-start))