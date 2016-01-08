import sys
board = "...........................OX......XO..........................."

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
        paths = [path for path in paths if path]
    for path in paths:
        path = sorted(path)
        if i > path[0]:
            path = path[::-1]
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

def findPossible(board, side):
    global cellPaths, oppositeSide

    opposite = oppositeSide[side]
    possible = set()
    sidePos = {pos for pos in range(64) if board[pos] == side}
    for pos in sidePos:
        for path in cellPaths[pos]:
            index = 1
            # if board[path[0]] != side:
            #     path = path[::-1]
            if board[path[index]] == opposite and '.' in [board[path[i]] for i in range(1, len(path))]:
                while board[path[index]] == opposite:
                    index += 1
                possible.add(path[index])
    return possible

def negascout(board, depth, alpha, beta, side):
    possible = {}
    possible['X'] = findPossible(board, 'X')
    possible['O'] = findPossible(board, 'O')
    opposite = oppositeSide[side]

    if depth == 0 or (len(possible['X']) == 0 and len(possible['O']) == 0):
        return board.count(side)
    first = True
    for pos in possible[side]:
        child = board[:pos] + side + board[pos+1:]
        if first == True:
            first = False
            score = -negascout(child, depth-1, -alpha-1, -alpha, opposite)
            if alpha < score < beta:
                score = -negascout(child, depth-1, -beta, -alpha, opposite)
        else:
            score = -negascout(child, depth-1, -beta, -alpha, opposite)
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    return alpha

display(board)
side = 'X'
canMove = True
while canMove:
    possible = {}
    possible['X'] = findPossible(board, 'X')
    possible['O'] = findPossible(board, 'O')
    opposite = oppositeSide[side]

    if len(possible['X']) == 0 and len(possible['O']) == 0:
        canMove = False
        continue

    if len(possible[side]) == 0:
        print("{} cannot move.".format(side))
        side = opposite
        continue
    print("====== {}'s Turn ======".format(side))
    negas = {}
    for pos in possible[side]:
        child = board[:pos] + side + board[pos+1:]
        negas[pos] = negascout(child, 5, float("-inf"), float("inf"), side)
    maximum = float("-inf")
    for pos in negas:
        if negas[pos] > maximum:
            maximum = negas[pos]
            maxpos = pos
    movePos = maxpos   

    board = board[:movePos] + side + board[movePos+1:]
    
    
    flip = set()
    for path in cellPaths[movePos]:
        # if board[path[0]] != side:
        #     path = path[::-1]
        # for i in range(1, len(path)):
        #     if
        
        
        
        index = 1
        if board[path[0]] != side:
            path = path[::-1]
        if board[path[index]] == opposite and side in [board[path[i]] for i in range(1, len(path))]:
            temp = set()
            while board[path[index]] == opposite:
                temp.add(path[index])
                index += 1
            if board[path[index]] == side:
                flip |= temp
     
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
