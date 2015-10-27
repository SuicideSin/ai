import sys, urllib.request, time, pickle
start = time.clock()

visited = []
'''
1. Find diameter of graph
FIND SPEED OF BFS in big O
'''

def bfs(n, adj, ret):
    level = {n: 0}
    distance = {0: [n]}
    parent = {n: None}
    visited.append(n)
    i = 1
    layer = [n]
    last = n
    while layer:
        next = []
        for u in layer:
            for v in adj[u]:
                if v not in level:
                    visited.append(v)
                    level[v] = i
                    if i not in distance:
                        distance[i] = []
                        distance[i].append(v)
                    else:
                        distance[i].append(v)
                    parent[v] = u
                    next.append(v)
                    last = v
        layer = next
        i += 1
    if ret is "length":
        return len(level)
    if ret is "parent":
        return parent
    if ret is "level":
        return level
    if ret is "distance":
        return distance
    if ret is "last":
        return last

wordList = pickle.load( open( 'wordladder.pkl' , 'rb' ) )
edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)

freq = {}
maxSize = 0
maxDiameter = 0
for k in wordList:
    if k not in visited:
        u = bfs(k, wordList, "last")
        v = bfs(u, wordList, "last")
        #print("U: {}; V: {}".format(u, v))
        level = bfs(u, wordList, "level")
        diameter = level[v]
        if diameter > maxDiameter:
            maxDiameter = diameter
        kLength = bfs(k, wordList, "length")
        if kLength > maxSize:
            maxSize = kLength
        if kLength not in freq:
            freq[kLength] = 1
        else:
            freq[kLength] += 1


print("{} words in list.".format(wordCount))
print("{} edges in graph.".format(edgeCount))
print("Compenent size frequency dictionary: {}".format(freq))
print("Size of largest component: {}".format(maxSize))
print("Diameter: {}".format(maxDiameter))

print("Completed in {} seconds.".format(time.clock()-start))
