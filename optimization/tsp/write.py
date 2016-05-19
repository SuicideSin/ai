#!/usr/local/bin/python3
import sys, ast, math, subprocess, os, time

path = [int(i) for i in ast.literal_eval(sys.argv[1])]
n = len(path)
def dist(t1, t2): return math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2)

cities = {i: j for (i, j) in enumerate((tuple([float(i) for i in line.rstrip('\n').split()])) for line in open('{}cities.txt'.format(len(path)), 'r')) if len(j) > 1}
cityCosts = {i: {j: dist(cities[i], cities[j]) for j in cities if j != i} for i in cities}

def cost(path, n): return sum([dist(cities[path[i]], cities[path[i+1]]) for i in range(-1, n-1)])
def allSwaps(path, n): return {i for i in {tuple(path[:i] + [path[j]] + path[i+1:j] + [path[i]] + path[j+1:]) for i in range(n) for j in range(n)} if len(i) == n}

def allReversals(path, n): return {i for i in {tuple(path[:i] + path[i:j+1][::-1] + path[j+1:]) for i in range(n) for j in range(n)} if len(i) == n}

def hillClimb(path, n):
    visited = set()
    c, p = cost(path, n), float("inf")
    while c < p:
        costDict = {i: cost(i, n) for i in allReversals(path, n) if i not in visited}
        path = list(min(costDict, key=costDict.get))
        p, c = c, cost(path, n)
        print(path)
        print(c)
    return path

def form(path, n):
    i = path.index(1)
    path = list(path[i:] + path[:i])
    if path[1] > path [-1]:
        path = [path[0]] + [path[i] for i in range(n-1, 0, -1)]
    return path
path = form(path, len(path))

def results(n, func, name, args):
    tick = time.clock()
    s = form(n, func(*args))
    assert len(s) == len(set(s))
    tock = time.clock()
    print("{}\n\033[1;32m{}\033[0m:\n{}\nTotal distance: {}\nFound in {} seconds.".format("-"*cols, name, s, cost(s, n), tock-tick))
    return s

#hc = results(n, hillClimb, "Untangled", (path, n))
f = open('hcdata.txt', 'w+')
for i in path:
    f.write("{}\t{}\n".format(round(cities[i][0]), (cities[i][1])))
f.write("{}\t{}\n".format(round(cities[1][0]), (cities[1][1])))

print(cost(path, len(path)))
#
# os.system("gnuplot ~/dev/school/ai/optimization/tsp/graph.gnu && display ~/dev/school/ai/optimization/tsp/hc.png")

print(form(path, len(path)))
