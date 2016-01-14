import sys, time
from tqdm import tqdm
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

def coord(position):
    return(int(pos/8), pos%8)

def display(*args):
    board = {i: args[0][i] for i in range(len(args[0]))}

    if len(args) == 2:
        for i in board:
            if i in args[1]:
                board[i] = '\033[32m*\033[0m'
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

def findPossible(board, side):
    global cellPaths, oppositeSide

    opposite = oppositeSide[side]
    allPos = [pos for pos in range(64) if board[pos] == side]
    possible = {}

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
                        possible[pathPos] = path
                    break
    return possible

def negascout(board, depth, alpha, beta, side):
    possible = {}
    possible['X'], possible['O'] = findPossible(board, 'X'), findPossible(board, 'O')
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

def alphabeta(board, depth, alpha, beta, onside, side):
    possible = {}
    possible['X'], possible['O'] = findPossible(board, 'X'), findPossible(board, 'O')
    opposite = oppositeSide[side]
    if depth == 0 or (len(possible['X']) == 0 and len(possible['O']) == 0):
        return board.count(side)
    if onside:
        v = float("-inf")
        for pos in possible[side]:
            child = flipBoard(board, pos, side)
            v = max(v, alphabeta(child, depth -1, alpha, beta, False, side))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    else:
        v = float("inf")
        for pos in possible[opposite]:
            child = board[:pos] + opposite + board[pos+1:]
            v = min(v, alphabeta(child, depth-1, alpha, beta, True, side))
            beta = min(v, beta)
            if beta <= alpha:
                break
        return v

def nextMove(board, side, possible):
    cornerPos = [0, 7, 56, 63]
    sidePos = [i for i in range(7)] + [i for i in range(0,63,8)] + [i for i in range(7,63,8)] + [i for i in range(56,64)]
    corners = [i for i in cornerPos if i in possible[side]]
    sides = [i for i in sidePos if i in possible[side] and i not in [1, 8, 6, 15, 48, 57, 62, 55]]
    if corners:
        movePos = corners[randint(0, len(corners)-1)]
    elif sides:
        movePos = sides[randint(0, len(sides)-1)]
    else:
        movePos = None
        negas = {}
        for pos in possible[side]:
            child = board[:pos] + side + board[pos+1:]
            negas[pos] = negascout(child, 2, float("-inf"), float("inf"), side)
        movePos = max(negas.keys(), key=(lambda key: negas[key]))
    return movePos

def randMove(board, side, possible):
    rand = randint(0, len(possible[side]))
    i = 0
    for pos in possible[side]:
        movePos = pos
        if i == rand:
            break
        i += 1
    return movePos

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
mult = False
smart = None
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'pvc':
        pvc = True
    elif sys.argv[1].lower() == 'cvc':
        cvc = True
        if len(sys.argv) > 2:
            mult = True
            smart = sys.argv[3].upper()
else:
    pvp = True

def othello():
    board = "...........................OX......XO..........................."
    if not mult:
        display(board)
    player = 'X'
    if pvc:
        player = input("Please choose a side (X or O): ").upper()
    side = 'X'
    canMove = True
    ply = 1
    while canMove:
        possible = {}
        possible['X'], possible['O'] = findPossible(board, 'X'), findPossible(board, 'O')
        opposite = oppositeSide[side]

        if len(possible['X']) == 0 and len(possible['O']) == 0:
            canMove = False
            continue

        if len(possible[side]) == 0:
            if not mult:
                print("{} cannot move.".format(side))
            side = opposite
            continue
        if not mult:
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
                if response == '.':
                    display(board, possible[side])
                if (' ' or ',' in response) and len(move) == 2 and len(response) > 2:
                    #print(len(response))
                    position = move[0] * 8 + move[1]
                elif len(response) == 2 and len(move) == 2:
                    position = int(response)
                if position in possible[side]:
                    movePos = position
                    invalid = False
                else:
                    print("Invalid move.")

        elif pvc:
            movePos = nextMove(board, side, possible)

        elif cvc:
            tick = time.clock()
            if smart:
                if side == smart:
                    movePos = nextMove(board, side, possible)
                else:
                    movePos = randMove(board, side, possible)
            else:
                movePos = nextMove(board, side, possible)

            tock = time.clock()

        newBoard = flipBoard(board, movePos, side)
        flip = [i for i in range(64) if board[i] != newBoard[i] and i != movePos]
        board = newBoard
        if not mult:
            display(board, flip, movePos)
        #print("%fseconds"%(tock - tick))
        side = opposite
        ply += 1

    scores = {}
    scores['X'] = board.count("X")
    scores['O'] = board.count("O")

    winner = max(scores.keys(), key=(lambda key: scores[key]))
    loser = oppositeSide[winner]

    if not mult:
        if scores['X'] == scores['O']:
            print("No winner. Both players scored {}.".format(scores[winner]))
        else:
            print("{} wins {} to {}.".format(winner, scores[winner], scores[loser]))

    return scores

if mult:
    trials = int(sys.argv[2])
    points = {'X':0,'O':0}
    wins = {'X':0,'O':0}
    ties = 0
    for i in tqdm(range(trials), desc="CvC Trials"):
        scores = othello()
        if scores['X'] == scores['O']:
            ties += 1
        else:
            winner = max(scores.keys(), key=(lambda key: scores[key]))
            loser = oppositeSide[winner]
            wins[winner] += 1
            points[winner] += scores[winner]
            points[loser] += scores[loser]

    xavg = points['X']/trials
    oavg = points['O']/trials

    print("X won {} times with an average of {} tiles.".format(wins['X'], xavg))
    print("O won {} times with an average of {} tiles.".format(wins['O'], oavg))
    print("{} ties.".format(ties))

else:
    othello()
