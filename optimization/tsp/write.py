#!/usr/local/bin/python3
import sys, ast, math, subprocess, os
path = [int(i) for i in ast.literal_eval(sys.argv[1])]
def dist(t1, t2): return math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2)

cities = {i: j for (i, j) in enumerate((tuple([float(i) for i in line.rstrip('\n').split()])) for line in open('{}cities.txt'.format(len(path)), 'r')) if len(j) > 1}
cityCosts = {i: {j: dist(cities[i], cities[j]) for j in cities if j != i} for i in cities}
def cost(path, n): return sum([cityCosts[path[i]][path[i+1]] for i in range(-1, n-1)])
def form(path, n):
    i = path.index(1)
    path = list(path[i:] + path[:i])
    if path[1] > path [-1]:
        path = [path[0]] + [path[i] for i in range(n-1, 0, -1)]
    return path
path = form(path, len(path))

f = open('hcdata.txt', 'w+')
for i in path:
    f.write("{}\t{}\n".format(round(cities[i][0]), (cities[i][1])))
f.write("{}\t{}\n".format(round(cities[1][0]), (cities[1][1])))

print(cost(path, len(path)))
#
# os.system("gnuplot ~/dev/school/ai/optimization/tsp/graph.gnu && display ~/dev/school/ai/optimization/tsp/hc.png")

print(form(path, len(path)))
