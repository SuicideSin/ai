import sys

def display(board):
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



if len(sys.argv) > 1:
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
