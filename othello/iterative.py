import sys, time

cellNeighbors = {i: {j for j in range(64) if j!=i and (abs(int(j/8)-int(i/8)) <= 1 and abs((j%8)-(i%8)) <= 1) } for i in range(64)}

# cellStraights = {i: {j for j in range(64) if j!=i and (int(j/8)==int(i/8) or (j%8)==(i%8) or ((abs(int(j/8)-int(i/8)) == abs((j%8)-(i%8)))))} for i in range(64)}

cellPaths = {}
#Perhaps make cellPaths a dictionary of 8 sets. each set is one direction from the origin. all new positions in the recursive function must go into the correct set.

for i in range(64):
    paths = [[] for j in range(8)]
    for j in range(64):
        jrow = int(j/8)
        jcol = j%8
        irow = int(i/8)
        icol = i%8
        
        if j == i:
            for k in range(8):
                paths[k].append(j);
        
        #same row to the left
        elif jrow == irow and jcol < icol:
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

if len(sys.argv) == 2:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1].upper()
        valid = True
        for char in board:
            if char != 'X' and char != 'O' and char != '.':
                valid = False
                print("Invalid Board.")
                break
        if valid:
            display(board)

def findPossible(board, side):
    global cellPaths, oppositeSide

    opposite = oppositeSide[side]
    possible = set()
    sidePos = {pos for pos in range(64) if board[pos] == side}
    for pos in sidePos:
        for path in cellPaths[pos]:
            index = 1
            if board[path[0]] != side:
                path = path[::-1]
            if board[path[index]] == opposite and '.' in [board[path[i]] for i in range(1, len(path))]:
                while board[path[index]] == opposite:
                    index += 1
                possible.add(path[index])
    return possible

if len(sys.argv) == 3:
    side = sys.argv[2].upper()
    board = sys.argv[1].upper()
    if len(board) > 64:
        print("Input board is too long.")
    else:
        display(board)
        start = time.clock()
        possible = findPossible(board, side)
        total = time.clock()-start
        print(possible)
        display(board, possible, side)
        print("Completed in %f seconds." % (total))
