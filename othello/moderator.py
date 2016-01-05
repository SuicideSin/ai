import sys
board = "...........................OX......XO..........................."

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

    if len(args) == 3:
        for i in args[1]:
            board[i] = '\033[32m' + args[2] + '\033[0m'

    for i in board:
        if board[i] == "X":
            board[i] = '\033[36mX\033[0m'
        elif board[i] == "O":
            board[i] = '\033[33mO\033[0m'

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
        visited[origin] = None
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

def packPossible(board, side):
    paths = []

    xPossible = set()
    xPos = {i for i in range(len(board)) if board[i] == "X"}
    for pos in xPos:
        findPossible(board, None, pos, {}, {}, xPossible)
    oPossible = set()
    oPos = {i for i in range(len(board)) if board[i] == "O"}
    for pos in oPos:
        findPossible(board, None, pos, {}, {}, oPossible)

    for i in range(len(board)):
        if board[i] == side:
            path = {}
            findPossible(board, None, i, path, {}, set())
            paths.append(path)

    return (xPossible,oPossible, paths)

display(board)
#side = input("Please enter the first player: ")
side = "X"
canMove = True
while canMove:
    possible = {}
    possible['X'], possible['O'], paths = packPossible(board, side)
    opposite = oppositeSide[side]

    if len(possible['X']) == 0 and len(possible['O']) == 0:
        canMove = False
        continue

    if len(possible[side]) == 0:
        print("{} cannot move.".format(side))
        side = opposite
        continue

    print("====== {}'s Turn ======".format(side))
    invalid = True
    movePos = 0
    while invalid:
        response = input("Please enter a move in row, col format: ")
        move = [int(response[i]) for i in range(len(response)) if response[i] in "1234567890"]
        if (' ' or ',' in response) and len(move) == 2 and len(response) > 2:
            #print(len(response))
            position = move[0] * 8 + move[1]
        elif len(response) == 2 and len(move) == 2:
            position = int(response)
        else:
            print("Invalid move. Try again.")
        if position in possible[side]:
            movePos = position
            invalid = False
        else:
            print("Invalid move. Try again.")

    board = board[:movePos] + side + board[movePos+1:]
    flip = set()
    for path in paths:
        if movePos in path:
            parent = path[movePos]
            while parent is not None:
                flip.add(parent)
                parent = path[parent]
    for pos in flip:
        board = board[:pos] + side + board[pos+1:]



    display(board)
    side = opposite


xc = board.count("X")
oc = board.count("O")

if xc > oc:
    print("X wins {} to {}.".format(xc, oc))
elif oc > xc:
    print("O wins {} to {}.".format(oc, xc))
elif xc == oc:
    print("No winner. Both players scored {}.".format(xc))
