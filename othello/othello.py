import sys

cellNeighbors = {i: {j for j in range(64) if j==i+8 or j==i-8 or j==i-1 or j==i+1 or j==i+9 or j==i+7 or j==i-9 or j==i-7 } for i in range(64)}

def display(board):
    border = ["-" for i in range(24)]
    border = "   {}".format("".join(border))
    print(border)
    for i in range(8):
        row = [board[j+8*i] for j in range(8)]
        row = "{} | {} | {}".format(i, "  ".join(row).upper(), i)
        print(row)
    print(border)
    cols = [str(i) for i in range(8)]
    cols = "{}  {}".format("  ", "  ".join(cols))
    print(cols)


if len(sys.argv) == 2:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1]
        valid = True
        for char in board:
            up = char.upper()
            if up != 'X' and up != 'O' and up != '.':
                valid = False
                print("Invalid Board.")
                break
        if valid:
            display(board)

def findPossible(board, pos, side):
    global cellNeighbors
    global possible
    
    '''
        Only recurse to positions that are direcly opposite the original pos!!! this way there is a straight path and not just neighbors

    '''

    if pos not in range(64):
        return ""
    if board[pos] == ".":
        return ""
    for i in cellNeighbors[pos]:
        fp = findPossible(board, i, side)
        if fp != "":
          return fp


if len(sys.argv) == 3:
    side = sys.argv[2]
    board = sys.argv[1]
    sidePos = [i for i in range(len(board)) if board[i]==side]
    possible = []
    for pos in sidePos:
        possible.append(findPossible(board, pos, side))
    display(board)
    print(possible)

    
#print(cellNeighbors)


















#eof
