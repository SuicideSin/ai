'''
38 cities 
Read in each city from file, make a dictionary
create list
e.g. [1, 12, 27, ... 6, 32, 25]
find total distance traveled


In a convex quadrilateral, the sum of the diagonals is always greater than the sum of any pair of opposite sides

Crossing paths is not optimal!

To uncross paths, flip the substring between 2 crossing points
e.g.

|-----q-d-----b-y-----|   1...xaby....pcdq.....1
|        \   /        |
|          /          |
|        /   \        |
|_____x-a-----c-o-----|

|-----q-d-----b-y-----|   1...xacp....ybdq.....1
|                     |
|                     |
|                     |
|_____x-a-----c-o-----|

reversing this string:
path[:b] + path[b:c+1][::-1] + path[c+1:]


How to check if two paths are crossing?

First we must find the area of a triangle:
Perhaps heron's formula: https://upload.wikimedia.org/math/d/8/5/d858202192abadd0bb8a60fa9dd9b013.png
... NAH

Use this:
|
|
|  . (1,4)
|
|
|.(0,1)   (3,0)  
|______._________________


A = 1/2 | 3 -1  0 |
        | 1  3  0 |
        | i  j  k |
        
OR:
SHOELACE THEOREM:
Inside the matrix are the coordinates of each vertex.

1/2 | 1  0 |
    | 3  0 |
    | 1  4 |
    | 0  1 |
    
    Compute pairwise products going in one direction minus pairwise products going in opposite direction
     = 1/2(0 + 12 + 1 + 0) - 1/2(0 + 0 + 0 + 1) 
     = 1/2(12)
     = 6
    
    
    d
    |       a
    |        \
    c         b
    
    A(a,b,c)
    A(a,b,d)
    If they have the same sign, then a,b and c,d are not intersecting
    If different sign, they are intersecting
    
    
Instead of doing all swaps, do all possible reversals (uncrossings)

Consider all pairs of positions, reverse the strings, find total distance, and compare whether new version is better or worse, keep if better

HINT: You don't have to recompute the WHOLE distance. You only have to compute the distance of the changed portions of the path.



|-----q-d-----b-y-----| 
|        \   /        |
|          /          |
|        /   \        |
|_____x-a-----c-o-----|

incrDist = d(a,c) + d(b,d) - d(a,b) - d(c,d)

threshold = .001

improvementNoted = True
while improvementNoted:
    improvementNoted = False
    for edge1 in range ( ):
        for edge2 in range( edge1+2,-):
            incrementalDist =  d(a,c) + d(b,d) - d(a,b) - d(c,d)
            if incrementalDist > -threshold: continue
            update path
            update distance
            improvementNoted = True
        if improvementNoted == True: break

more improvement:
-improve distance measurement
-

'''

def allPerms(perm):
    if len(perm) == 0: return [[]]
    if len(perm) == 1: return [perm]                #optional
    if len(perm) == 2: return [perm, perm[::-1]]    #optional
    answer = []
    for i in range(len(perm)):
        subPerm = allPerms(perm[:i] + perm[i+1:])
        subPerm = [lst + [perm[i]] for lst in subPerm]
        answer += subPerm
    return answer

def findAdjSwapPerms(n):
    #finds positions for adjacent swaps that will generate all n! permutations of [0...n-1]
    if n == 1: return []
    if n == 2: return [0, 0] #optional
    fs = findAdjSwapPerms(n-1)
    pfx = [[i for i in range(n-1)], [i for i in range(n-1)][::-1]]
    fsr = [pfx[i%2] + [fs[i] + (i%2)] for i in range(len(fs))]
    return [elem for frssub in fsr for slem in fsrsub]