import sys, urllib.request, time, pickle
startTime = time.clock()

wordList = pickle.load( open( 'wordladder.pkl' , 'rb' ) )
edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)




print("{} vertices in graph.".format(wordCount))
print("{} edges in graph.".format(edgeCount))

startTime = time.clock()

if len(sys.argv) == 3:

    start = sys.argv[1]
    target = sys.argv[2]

    visited = []
    parent = {target:None}
    def DFS(V, adj, s):
        for v in adj[s]:
            if v not in parent:
                visited.append(v)
                parent[v] = s
                DFS(V, adj, v)

    DFS(start, wordList, target)

    if start in parent:
        child = start
        path = [start]
        while parent[child] not in target:
            parentV = parent[child]
            path.append(parentV)
            child = parentV
        path.append(target)
        print(path)
        print("{} vertices visited.".format(len(visited)))
    else:
        print("Words are not connected")

print("Completed in {} seconds.".format(time.clock()-startTime))
