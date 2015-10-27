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
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def astar( graph, start, end ):
    frontier = queue.PriorityQueue()
    frontier.put(start, 0)
    path = {}
    gcost = {}
    path[start] = None
    gcost[start] = 0
    max = 0
    popped = 0

    while not frontier.empty():

        if frontier.qsize() > max:
            max = frontier.qsize()


        current = frontier.get()
        #popped += 1


        if current == end:
            print("Distance from {} to {}: {}".format(start, end, gcost[current]))
            #printpath(start, end, path)

            print("{} nodes visited.".format(len(path)))
            print("Max queue size: {}".format(max))
            print("Size of closed set: {}".format(popped))

            break

        for neighbor in graph[current]:
            g = gcost[current] + graph[current][neighbor]
            if neighbor not in gcost or g < gcost[neighbor]:
                gcost[neighbor] = g
                f = g + heuristic(neighbor, end)
                frontier.put(neighbor, f)
                path[neighbor] = current
                popped += 1





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
