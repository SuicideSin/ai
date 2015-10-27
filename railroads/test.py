import sys, urllib.request, time, pickle, queue
from math import pi, acos, sin, cos

def minimum( dic ):
    min = float("inf")
    node = None
    for vert in dic:
        if dic[vert] < min:
            min = dic[vert]
            node = vert
    return node

rails = pickle.load( open( 'rom.pkl' , 'rb' ) )
edgeCount = rails.pop("edges")[0]
nodeCount = len(rails)

nodes = pickle.load( open( 'romNodes.pkl' , 'rb' ) )


test = {'a': 21, 'b': 12, 'c': 5, 'd': 32, 'e': 7}

print(test)
while test:
    q = minimum(test)
    print(q)
    test.pop(q)
    print(test)
