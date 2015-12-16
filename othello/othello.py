import sys

cellNeighbors = {i: {j for j in range(64) if j!=i and (j==i+8 or j==i-8 or j==i-1 or j==i+1 or j==i+9 or j==i+7 or j==i-9 or j==i-7) } for i in range(64)}
cellStraights = {i: {j for j in range(64) if j!=i and (j%8==i%8 or int(j/8) == int(i/8))} for i in range(64)}
opposite = {"X": "O", "O":"X"}

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
        board = sys.argv[1].upper()
        valid = True
        for char in board:
            if char != 'X' and char != 'O' and char != '.':
                valid = False
                print("Invalid Board.")
                break
        if valid:
            display(board)

def findPossible(board, pos, origin, side):
    global cellNeighbors
    global possible

    opposite = opposite[side]
           
    if pos is None:
        if opposite not in board:
            return ""
        for pos in cellNeighbors[origin]:
            if board[pos] == opposite:
                return findPossible(board, pos, origin, side)
    
    if board[pos] == ".":
        possible.append(pos)
        return ""

    else:
        for i in cellNeighbors[pos]:
            pass 


if len(sys.argv) == 3:
    side = sys.argv[2].upper()
    board = sys.argv[1].upper()
    sidePos = [i for i in range(len(board)) if board[i]==side]
    possible = []
    display(board)
    for pos in sidePos:
        findPossible(board, None, pos, side)
    print(possible)

    
#print(cellNeighbors)
print(cellStraights)

















#eof
