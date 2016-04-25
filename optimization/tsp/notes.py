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


'''
