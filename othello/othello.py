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

def coord(position):
    return(int(pos/8), pos%8)

def display(*args):
    board = {i: args[0][i] for i in range(len(args[0]))}

    if len(args) == 3:
        for i in board:
            if i in args[1]:
                board[i] = '\033[32m' + board[i] + '\033[0m'
            if i == args[2]:
                board[i] = '\033[31m' + board[i] + '\033[0m'

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
    global cellNeighbors, cellPaths, oppositeSide

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

def negascout(board, depth, alpha, beta, side):
    possible = {}
    possible['X'], possible['O'], paths = packPossible(board, side)
    opposite = oppositeSide[side]

    if depth == 0 or (len(possible['X']) == 0 and len(possible['O']) == 0):
        return board.count(side)
    first = True
    for pos in possible[side]:
        child = flipBoard(board, pos, side)
        if first == True:
            first = False
            score = -negascout(child, depth-1, -alpha-1, -alpha, opposite)
            if alpha < score < beta:
                score = -negascout(child, depth-1, -beta, -alpha, opposite)
        else:
            score = -negascout(child, depth-1, -beta, -alpha, opposite)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return alpha

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

pvc = False
cvc = False
pvp = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'pvc':
        pvc = True
    elif sys.argv[1] == 'cvc':
        cvc = True
else:
    pvp = True

display(board)
player = 'X'
if pvc:
    player = input("Please choose a side (X or O): ").upper()
side = 'X'
canMove = True
ply = 1
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

    print("====== Ply {}: {}'s Turn ======".format(ply, side))
    '''print(possible[side])'''
    if (side == player and pvc) or pvp:
        invalid = True
        movePos = 0
        while invalid:
            response = input("Player {}, Please enter a move in row, col format: ".format(side))
            move = [int(response[i]) for i in range(len(response)) if response[i] in "1234567890"]
            position = -1
            if response.lower() in trans:
                tempboard = ""
                for pos in trans[response.lower()]:
                    tempboard += board[pos]
                display(tempboard)
            if (' ' or ',' in response) and len(move) == 2 and len(response) > 2:
                #print(len(response))
                position = move[0] * 8 + move[1]
            elif len(response) == 2 and len(move) == 2:
                position = int(response)
            if position in possible[side]:
                movePos = position
                invalid = False
    
    elif pvc or cvc:
        negas = {}
        for pos in possible[side]:
            child = board[:pos] + side + board[pos+1:]
            negas[pos] = negascout(child, 4, float("-inf"), float("inf"), side)
        maximum = float("-inf")
        for pos in negas:
            if negas[pos] > maximum:
                maximum = negas[pos]
                maxpos = pos
        movePos = maxpos   
        #print("{} Moves to {},{}".format(side, int(movePos/8), movePos%8))

    newBoard = flipBoard(board, movePos, side)
    flip = [i for i in range(64) if board[i] != newBoard[i] and i != movePos]
    board = newBoard
    display(board, flip, movePos)
    side = opposite
    ply += 1


xc = board.count("X")
oc = board.count("O")

if xc > oc:
    print("X wins {} to {}.".format(xc, oc))
elif oc > xc:
    print("O wins {} to {}.".format(oc, xc))
elif xc == oc:
    print("No winner. Both players scored {}.".format(xc))
