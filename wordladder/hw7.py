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


def minimum(dist):
	vert = 'undefined'
	best = 9999999
	for v in dist:
		if dist[v] < best:
			vert = v
			best = dist[v]
	return vert


def dijkstra(graph,v,t):
	currentdist = {}
	currentdist[v] = 0
	dist = {}
	max = 0
	popped = 0
	path = {v: None}

	while len(dist) < len(graph):
		cur = minimum(currentdist)
		if len(graph) - len(dist)  > max:
			max = len(graph) - len(dist)
		if cur == t:
			print()
			print("Maximum queue size: {}".format(max))
			print("Number of nodes popped: {}".format(popped))
			print("Distance from {} to {} is {}".format(v, t, currentdist[cur]))
			printpath(v, t, path)
			break
		if(cur == 'undefined'):
			break
		dist[cur] = currentdist[cur]
		del currentdist[cur]
		popped += 1

		for x in graph[cur]:
			if x not in dist:
				if x not in currentdist:
					currentdist[x] = dist[cur] + graph[cur][x]
					path[x] = cur
				# elif dist[cur] + graph[cur][x] < currentdist[x]:
				# 	currentdist[x] = dist[cur] + graph[cur][x]
	if t not in currentdist:
		print("{} and {} are NOT connected!".format(v, t))
	return dist



wordList = pickle.load( open( 'weightedwordladder.pkl' , 'rb' ) )
edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)

if len(sys.argv) > 2:
	dijkstra(wordList, sys.argv[1], sys.argv[2])
else:
	print("No inputs entered.")


print("{} words in list.".format(wordCount))
print("{} edges in graph.".format(edgeCount))
print("Completed in {} seconds.".format(time.clock()-start))
print()
