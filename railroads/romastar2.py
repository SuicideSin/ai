import sys, urllib.request, time, pickle, queue
from math import pi, acos, sin, cos
start = time.clock()

def minimum( dic ):
    min = float("inf")
    node = None
    for vert in dic:
        if dic[vert] < min:
            min = dic[vert]
            node = vert
    return node

def heuristic( current, target ):
    y1 = nodes[current][0]
    x1 = nodes[current][1]
    y2 = nodes[target][0]
    x2 = nodes[target][1]
    R = 3958.7613
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def astar( graph, start, end ):
    open = { start: 0 }
    closed = {}
    g = { start: 0 }
    h = { start: heuristic(start, end) }
    f = { start: g[start] + h[start] }
    yes = True
    min = float("inf")

    while open:
        q = minimum(open)
        open.pop(q)

        if q==end:
            print(g[q])
            break

        for neighbor in graph[q]:
            g[neighbor] = g[q] + graph[q][neighbor]
            h[neighbor] = heuristic(neighbor, end)
            f[neighbor] = g[neighbor] + h[neighbor]

            if neighbor in open and open[neighbor] < f[neighbor]:
                    continue
            if neighbor in closed and closed[neighbor] < f[neighbor]:
                    continue

            open[neighbor] = f[neighbor]

        closed[q] = f[q]

rails = pickle.load( open( 'rom.pkl' , 'rb' ) )
edgeCount = rails.pop("edges")[0]
nodeCount = len(rails)

nodes = pickle.load( open( 'romNodes.pkl' , 'rb' ) )

if len(sys.argv) > 2:
	astar(rails, sys.argv[1], sys.argv[2])


print("{} nodes in network.".format(nodeCount))
print("{} edges in network.".format(edgeCount))
print("Completed in {} seconds.".format(time.clock()-start))
print()
