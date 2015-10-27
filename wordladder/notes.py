'''
How to speed up wordladder:
1. Save structure to file with pickle
  use pickle dump and load
2. BAD: print("Length" + str(len(myDict)))
  GOOD: print("Length: {}".format(len(myDict)))
3. File location = sys.argv[0]+"//..//words.txt"
4. Generate every single permutation, and check if each permutation is in the list
    5000*150
5. attle -> [battle, cattle, rattle]
    ottle -> [bottle]
6. Dictionary lookup is SUPER FAST - consant time
    Try to make everything into a dictionary lookup
'''
#####################################################################
import time
startTime = time.clock()



print("Run time(sec): {}".format(time.clock()-startTime))

#####################################################################
wordList = open('words.txt', 'r').read().splitlines()
#####################################################################


'''
BFS:
    find all the components = O(|V| + |E|)
    find the longest shortest path from a vertex = O(E)
    find the shortest path between two vertices = O(E)
    find the diameter = O(VE)


DFS:
    import random
    random.shuffle(uList)




SEARCHES: (searching for a path from s to p)
1. BFS O(E)
2. Bidirectional BFS O(E)
3. DFS
4. DFS w/ iterative deepening
5. Dijkstra

HW DUE 9/28 -- Do Dijkstra, and do Bidirectional BFS and iterative deepening if
                time allows
                1. Find shortest path between two wordList
                2. Find the number of vertices visited
                3. Find maximum size of the queue
                4. The running time of the program

New edge case:
    Words like 'silver' and 'sliver' (adjacent characters are swapped),
    put edge between them and then add weighting of 5
    all other edges have weighting of 1

'''
    # def DFS(V, adj):
    #     parent = {}
    #     for s in V:
    #         if s not in parent:
    #             parent[s] = None
    #             DFSvisit(V, adj, s)



									running time	shortest path		queue size		verts visited
bfs										Y					Y											
bidirectional bfs						Y					Y											Y
dfs										Y					M					Y						
dfs iterative deepening				Y					Y					Y						
djikstra									Y					Y											

#Heuristic - an algorithm that is not guaranteed, but will probably do well
'''
	A* is a generalization of Dijkstra's algorithm
	



'''




















