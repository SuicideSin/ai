import sys, urllib.request, time, pickle
start = time.clock()
global visited
visited = []
'''
1. Number of components
2. Frequency dictionary of component size
3. Find the furthest word from a given input word
    give distance and path
4. Find the shortest path from word w1 to w2
    give distance and path
'''

def bfs(s, graph, ret):
    level = {s: 0}
    distance = {0: [s]}
    parent = {s: None}
    visited.append(s)
    i = 1
    layer = [s]
    while layer:
        next = []
        for u in layer:
            for v in graph[u]:
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

wordList = pickle.load( open( 'wordladder.pkl' , 'rb' ) )
edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)

freq = {}
max = 0
for k in wordList:
    if k not in visited:
        kLength = bfs(k, wordList, "length")
        if kLength > max:
            max = kLength
        if kLength not in freq:
            freq[kLength] = 1
        else:
            freq[kLength] += 1

print("{} words in list.".format(wordCount))
print("{} edges in graph.".format(edgeCount))
print("Compenent size frequency dictionary: {}".format(freq))
print("Size of largest component: {}".format(max))

if len(sys.argv) == 2:
    word1 = sys.argv[1]
    parent = bfs(word1, wordList, "parent")
    level = bfs(word1, wordList, "level")
    distance = bfs(word1, wordList, "distance")
    #print(distance)
    max = 0
    for dist in distance:
        if dist > max:
            max = dist
    print("Word(s) farthest from {}: {}".format(word1, distance[max]))
    for vert in distance[max]:
        print("Distance from {} to {}: {}".format(word1, vert, max))
        print("Path from {} to {}:".format(word1, vert))
        path = [word1]
        child = vert
        while parent[child] is not word1:
            parentV = parent[child]
            path.append(parentV)
            child = parentV
        path.append(vert)
        print()
        print(path[0], end="")
        for i in range(2, len(path)):
            k = len(path)-i
            print(" -- {}".format(path[k]), end="")
        print(" -- {}".format(path[len(path)-1]))

if len(sys.argv) == 3:
    word1 = sys.argv[1]
    word2 = sys.argv[2]
    parent = bfs(word1, wordList, "parent")
    level = bfs(word1, wordList, "level")
    distance = bfs(word1, wordList, "distance")
    #print(parent)
    if word2 not in level:
        print("{} and {} are not connected!".format(word1, word2))
    else:
        child = word2;
        path = [word1]
        print("Shortest distance between {} and {}: {}".format(word1, word2, level[word2]))
        while parent[child] is not word1:
            parentV = parent[child]
            path.append(parentV)
            child = parentV
        path.append(word2)
        print("Shortest path from {} to {}:".format(word1, word2))

        print(path[0], end="")
        for i in range(2, len(path)):
            k = len(path)-i
            print(" -- {}".format(path[k]), end="")
        print(" -- {}".format(path[len(path)-1]))

print("Completed in {} seconds.".format(time.clock()-start))
