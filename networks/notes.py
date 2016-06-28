'''

|v| = 40000
avg deg = 3
Number of edges = 3*40000/2 = 60000

Erdos-Renyi model
- Given the vertices, connect the edges at random

BA Model (Albert Barabasi and Reha Albert)
- The probability that a vertex is connected to another vertex, v, is give by the probabilty that is equal to (degree of v / sum of vertices in graph) = (degree of v / 2*Edges)


Homework - 
1. Build a network with 40,000 vertices
2. P(k) the # of vertices with degree k
3. Graph P(k) (normally normalized)
    Use some python library
4. Start with a connected graph of the (~2) vertices
    Each new vertex coming in should contribute m <= m0 edges
5. Total vertices and Total edges should be the same
    E = m*V
    E = V/2 * (average degrees)
    m = (average degrees)/2
'''

