import sys

cellNeighbors = {i: {j for j in range(64) if j!=i and (abs(int(j/8)-int(i/8)) <= 1 and abs((j%8)-(i%8)) <= 1) } for i in range(64)}

cellStraights = {i: {j for j in range(64) if j!=i and (int(j/8)==int(i/8) or (j%8)==(i%8) or ((abs(int(j/8)-int(i/8)) == abs((j%8)-(i%8)))))} for i in range(64)}

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

def findPossible(board, pos, origin, path, possible):
    global cellNeighbors, cellStraights, oppositeSide

    opposite = oppositeSide[board[origin]]

    if pos is None:
        if opposite not in board:
            return
        for pos in cellNeighbors[origin]:
            if board[pos] == opposite:
                path[pos] = origin
                findPossible(board, pos, origin, path, possible)

    elif board[pos] == "." and board[path[pos]] == opposite:
        possible.add(pos)
        return
    else:
        for i in cellNeighbors[pos]:
            if i not in path and i in cellStraights[origin]:
                path[i] = pos
                findPossible(board, i, origin, path, possible)

if len(sys.argv) == 3:
    side = sys.argv[2].upper()
    board = sys.argv[1].upper()
    sidePos = [i for i in range(len(board)) if board[i]==side]
    display(board)
    total = set()
    for pos in sidePos:
        possible = set()

        findPossible(board, None, pos, {}, possible)
        total = total | possible
        print(coord(pos))
        for pos in sorted(possible):
            print('\t{}'.format(coord(pos)))

    display(board, total, side)
