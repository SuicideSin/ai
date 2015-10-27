import sys
import urllib.request
import time
import pickle
from math import pi, acos, sin, cos
start = time.clock()

file = open('romNodes.txt', 'r')
nodes = {}
rails = {}

for line in file:
    node = line.split()
    nodes[node[0]] = [float(node[1]), float(node[2])]
    rails[node[0]] = {}

file2 = open('romEdges.txt', 'r')

edgecount = 0

for line in file2:
    edge = line.split()
    node1 = edge[0]
    node2 = edge[1]


    R = 3958.7613
    #R = 3958.76
    y1 = nodes[node1][0]
    x1 = nodes[node1][1]
    y2 = nodes[node2][0]
    x2 = nodes[node2][1]

    c = pi/180.0

    x1 *= c
    y1 *= c
    x2 *= c
    y2 *= c

    dist = acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

    rails[node1][node2] = dist
    rails[node2][node1] = dist
    edgecount += 1

rails["edges"] = [edgecount]

print(nodes)

fout = open( 'rom.pkl' , 'wb' )
pickle.dump( rails , fout , protocol = 2 )
fout.close()

fout = open( 'romNodes.pkl' , 'wb' )
pickle.dump( nodes , fout , protocol = 2 )
fout.close()

print(edgecount)
print(len(rails))
