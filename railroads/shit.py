import sys, urllib.request, time, pickle, queue
import heapq
from math import pi, acos, sin, cos
start = time.clock()

def printpath(v, t, path):
	path2 = [v]
	child = t
	while path[child] is not v:
		parentV = path[child]
		path2.append(parentV)
		child = parentV
	path2.append(t)
	print("Path from {} to {}:".format(v, t))
	print(path2[0], end="")
	if(len(path2) == 2):
		print(" -- {}".format(path2[1]))
	else:
		for i in range(2, len(path2)):
			k = len(path2)-i
			print(" -- {}".format(path2[k]), end="")
		print(" -- {}".format(path2[len(path2)-1]))

def heuristic( current, target ):
    y1 = nodes[current][0]
    x1 = nodes[current][1]
    y2 = nodes[target][0]
    x2 = nodes[target][1]
    R = 3958.7613
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def minimum(graph):
	min = float("inf")
	minNode = None
	for key in graph:
		if graph[key] < min:
			min = graph[key]
			minNode = key
	return key

def a_star(graph, start, goal):
	open = { start: 0 }
	closed = []

	g = { start: 0 }
	f = { start: heuristic(start, goal)}

	path = {start: None}

	while open:
		current = minimum(open)
		del open[current]

		if current == goal:
			print(g[current])
			break

		for neighbor in graph[current]:

			g[neighbor] = g[current] + graph[current][neighbor]
			cost = g[neighbor] + heuristic(neighbor, goal)


			if neighbor in open and f[neighbor] < cost:
				continue
			if neighbor in closed and f[neighbor] < cost:
				continue
			else:
				open[neighbor] = cost
				f[neighbor] = cost
				path[neighbor] = current
		closed.append(current)



wordList = pickle.load( open( 'rom.pkl' , 'rb' ) )
edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)

nodes = pickle.load( open( 'romNodes.pkl' , 'rb' ) )

if len(sys.argv) > 2:
	a_star(wordList, sys.argv[1], sys.argv[2])
else:
	print("No inputs entered.")


print("{} words in list.".format(wordCount))
print("{} edges in graph.".format(edgeCount))
print("Completed in {} seconds.".format(time.clock()-start))
print()
