import sys, urllib.request, time, pickle, queue
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

def dijkstra(graph,v,t):
	dist = {}
	currentdist = {}
	dist[v] = 0
	currentdist[v] = 0
	unvisited = []
	parents = {v: None}

	for vertex in graph:
		if vertex != v:
			dist[vertex] = float("inf")
		unvisited.append(vertex)
	current = v
	while unvisited:

		if current == t:
			printpath(v,t, parents)
			print(currentdist[current])

		min = float("inf")
		minNode = None
		for node in graph[current]:
			tentative = currentdist[current] + graph[current][node]
			if  tentative < dist[node]:
				dist[node] = tentative
				currentdist[node] = tentative
				parents[node] = current
			if currentdist[node] < min and node in unvisited:
				min = tentative
				minNode = node
		print(current)
		unvisited.remove(current)
		current = minNode
		currentdist[current] = min




rails = pickle.load( open( 'rom.pkl' , 'rb' ) )
edgeCount = rails.pop("edges")[0]
nodeCount = len(rails)

if len(sys.argv) > 2:
	dijkstra(rails, sys.argv[1], sys.argv[2])


print("{} nodes in network.".format(nodeCount))
print("{} edges in network.".format(edgeCount))
print("Completed in {} seconds.".format(time.clock()-start))
