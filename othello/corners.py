import sys
from random import randint

cellPaths = {}
for i in range(64):
    paths = [[] for j in range(8)]
    for j in range(64):
        jrow = int(j/8)
        jcol = j%8
        irow = int(i/8)
        icol = i%8
        #same row to the right
        if jrow == irow and jcol > icol:
            paths[1].append(j)
        #same col upward
        elif jcol == icol and jrow > irow:
            paths[2].append(j)
        #diagonals
        elif abs(jrow - irow) == abs(jcol - icol):
            #SW
            if jrow > irow and jcol < icol:
                paths[6].append(j)
            #SE
            if jrow > irow and jcol > icol:
                paths[7].append(j)
        k = abs(j-63)
        krow = int(k/8)
        kcol = k%8
        irow = int(i/8)
        icol = i%8
        #same row to the left
        if krow == irow and kcol < icol:
            paths[0].append(k)
        #same col downward
        elif kcol == icol and krow < irow:
            paths[3].append(k)
        #diagonals
        elif abs(krow - irow) == abs(kcol - icol):
            #NW
            if krow < irow and kcol < icol:
                paths[4].append(k)
            #NE
            if krow < irow and kcol > icol:
                paths[5].append(k)
    paths = [path for path in paths if path]
    cellPaths[i] = paths

oppositeSide = {"X": "O", "O":"X"}

i = [i for i in range(64)]
rl = [pos for arr in [[j for j in range(64) if j%8 == abs(i-7)] for i in range(8)] for pos in arr]
rr = [pos for arr in [[abs(j-63) for j in range(64) if abs(j-63)%8 == i] for i in range(8)] for pos in arr]
r2 = [pos for arr in [[abs(j-63) for j in range(64) if int(abs(j-63)/8) == abs(i-7)] for i in range(8)] for pos in arr]
fx = [pos for arr in [[j for j in range(64) if int(j/8) == abs(i-7)] for i in range(8)] for pos in arr]
fy = [pos for arr in [[abs(j-63) for j in range(64) if int(abs(j-63)/8) == i] for i in range(8)] for pos in arr]
fd = [pos for arr in [[abs(j-63) for j in range(64) if abs(j-63)%8 == abs(i-7)] for i in range(8)] for pos in arr]
fo = [pos for arr in [[j for j in range(64) if int(j%8) == i] for i in range(8)] for pos in arr]

trans = {"i":i, "rl":rl, "rr":rr, "r2":r2, "fx":fx, "fy":fy, "fd":fd, "fo":fo}

def findPossible(board, side):
    global cellPaths, oppositeSide

    opposite = oppositeSide[side]
    allPos = [pos for pos in range(64) if board[pos] == side]
    possible = set()

    for pos in allPos:
        for path in cellPaths[pos]:
            valid = False
            for pathPos in path:
                if board[pathPos] == opposite:
                    valid = True
                    continue
                elif board[pathPos] == side:
                    break
                elif board[pathPos] == '.':
                    if valid:
                        possible.add(pathPos)
                    break
    return possible

def nextMove(board, side, possible):
    cornerPos = [0, 7, 56, 63]
    corners = [i for i in cornerPos if i in possible]
    if corners:
        return corners[randint(0, len(corners)-1)]
    else:
        flips = {pos: flipBoard(board, pos, side) for pos in possible}
        return max(flips.keys(), key=(lambda key: flips[key]))

def flipBoard(board, move, side):
    opposite = oppositeSide[side]
    board = board[:move] + side + board[move+1:]
    flip = []
    paths = [path for path in cellPaths[move] if board[path[0]] == opposite]
    for path in cellPaths[move]:
        temp = []
        valid = False
        for pos in path:
            if board[pos] == '.':
                break
            elif board[pos] == side:
                valid = True
                break
            else:
                temp.append(pos)
        if valid:
            flip += temp
    for pos in flip:
        board = board[:pos] + side + board[pos+1:]

    return board

board = sys.argv[1]
side = sys.argv[2]

print(nextMove(board,side,findPossible(board, side)))