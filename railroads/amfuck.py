import sys, urllib.request, time, pickle, queue
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
    return (acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R)

def astar( graph, start, goal ):
	frontier = queue.PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0

	while not frontier.empty():
		current = frontier.get()

		if current == goal:
			print(len(came_from))
			print(cost_so_far[current])
			break

		for next in graph[current]:
			new_cost = cost_so_far[current] + graph[current][next]
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + heuristic(next, goal)
				frontier.put(next, priority)
				came_from[next] = current





rails = pickle.load( open( 'usa.pkl' , 'rb' ) )
edgeCount = rails.pop("edges")[0]
nodeCount = len(rails)

nodes = pickle.load( open( 'usaNodes.pkl' , 'rb' ) )

if len(sys.argv) > 2:
	astar(rails, sys.argv[1], sys.argv[2])


print("{} nodes in network.".format(nodeCount))
print("{} edges in network.".format(edgeCount))
print("Completed in {} seconds.".format(time.clock()-start))
print()
