import sys
board = "...........................XO......OX..........................."

cellNeighbors = {i: {j for j in range(64) if j!=i and (abs(int(j/8)-int(i/8)) <= 1 and abs((j%8)-(i%8)) <= 1) } for i in range(64)}
cellPaths = {}
for i in range(64):
    paths = [[] for j in range(8)]
    for j in range(64):
        jrow = int(j/8)
        jcol = j%8
        irow = int(i/8)
        icol = i%8
        #same row to the left
        if jrow == irow and jcol < icol:
            paths[0].append(j)
        #same row to the right
        elif jrow == irow and jcol > icol:
            paths[1].append(j)
        #same col upward
        elif jcol == icol and jrow > irow:
            paths[2].append(j)
        #same col downward
        elif jcol == icol and jrow < irow:
            paths[3].append(j)
        #diagonal
        elif abs(jrow - irow) == abs(jcol - icol):
            #NW
            if jrow < irow and jcol < icol:
                paths[4].append(j)
            #NE
            if jrow < irow and jcol > icol:
                paths[5].append(j)
            #SW
            if jrow > irow and jcol < icol:
                paths[6].append(j)
            #SE
            if jrow > irow and jcol > icol:
                paths[7].append(j)
    cellPaths[i] = paths
oppositeSide = {"X": "O", "O":"X"}

def coord(position):
    return(int(pos/8), pos%8)

def display(*args):
    board = {i: args[0][i] for i in range(len(args[0]))}
    if len(args) ==3:
        for i in args[1]:
            board[i] = '\033[32m' + args[2] + '\033[0m'

    border = ["-" for i in range(24)]
    border = "   {}".format("".join(border))
    print(border)
    for i in range(8):
        row = [board[j+8*i] for j in range(8)]
        row = "{} | {} | {}".format(i, "  ".join(row), i)
        print(row)
    print(border)
    cols = [str(i) for i in range(8)]
    cols = "{}  {}".format("  ", "  ".join(cols))
    print(cols)
    
def findPossible(board, pos, origin, visited, path, possible):
    global cellNeighbors, cellPaths, oppositeSide #, cellStraights

    opposite = oppositeSide[board[origin]]

    if pos is None:
        if opposite not in board:
            return
        for pos in cellNeighbors[origin]:
            if board[pos] == opposite:
                visited[pos] = origin
                path = []
                for route in cellPaths[origin]:
                    if pos in route:
                        path = route
                findPossible(board, pos, origin, visited, path, possible)

    elif board[pos] == "." and board[visited[pos]] == opposite:
        possible.add(pos)
        return
    else:
        for i in cellNeighbors[pos]:
            if i not in visited and i in path:
                visited[i] = pos
                findPossible(board, i, origin, visited, path, possible)

def packPossible(board):
    xPossible = set()
    xPos = {i for i in len(board) if board[i] == "X"}
    for pos in xPos:
        findPossible(board, None, pos, {}, {}, xPossible)
    oPossible = set()
    oPos = {i for i in len(board) if board[i] == "O"}
    for pos in oPos:
        findPossible(board, None, pos, {}, {}, oPossible)
    
display(board)
turn = input("Please enter the first player: ")
canMove = True
while canMove:
    xPossible, oPossible = packPossible(board)
    
    if len(xPossible) == 0 and len(oPossible) == 0:
        canMove = False
        continue
        
    if turn == "X" and len(xPossible) == 0:
        print("No possible moves for X. Turn passed.")
        continue
    if turn == "O" and len(oPossible) == 0:
        print("No possible moves for O. Turn passed.")
        continue
    
    invalid = True:
    while invalid:
        position = input("{}, please enter a move in r c format.")


xc = 0
oc = 0
for i in board:
    if i=="X":
        xc += 1
    if i=="O":
        oc += 1
if xc > oc:
    print("X wins  {} to {}.".format(xc, oc))
if oc > xc:
    print("O wins  {} to {}.".format(oc, xc))
else:
    print("No winner. Both players scored {}.".format(xc))