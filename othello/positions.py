import sys

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


opposite = {"X": "O", "O":"X"}

def coord(position):
    return(int(pos/8), pos%8)

def display(*args):
    board = {i: "".join(args[0][i]) for i in range(64)}
    board = {}
    for i in range(64):
        string = "".join(args[0][i])
        if len(string) == 2:
            board[i] = string
        else:
            board[i] = string + " "
    if len(args) ==3:
        for i in args[1]:
            board[i] = '\033[32m' + args[2] + '\033[0m'

    border = ["-" for i in range(32)]
    border = "   {}".format("".join(border))
    print(border)
    for i in range(8):
        row = ["" for i in range(8)]
        for j in range(8):
            x = board[j+8*i]
            if len(x) == 2:
                row[j] = x
            else:
                row[j] = x + " "
        row = "{} | {} | {}".format(i, "  ".join(row), i)
        print(row)
    print(border)
    cols = [str(i) for i in range(8)]
    cols = "{}  {}".format("  ", "   ".join(cols))
    print(cols)


display([str(i) for i in range(64)])

if len(sys.argv) > 1:
    if sys.argv[1] == "n":
        print(cellNeighbors)
        print(type(cellNeighbors[0].pop()))
        display([str(i) for i in range(64)])
        while True:
            index = input("Which index? ")
            pos = int(index)
            display([str(i) for i in range(64)], cellNeighbors[pos], ".")

    elif sys.argv[1] == "s":
        print(cellStraights)
        print(type(cellStraights[0].pop()))
        display([str(i) for i in range(64)])
        while True:
            index = input("Which index? ")
            pos = int(index)
            display([str(i) for i in range(64)], cellStraights[pos], ".")

    elif sys.argv[1] == "o":
        print(opposite)
    elif sys.argv[1] == "f":
        while True:
            board = "".join([str(i) for i in range(64)])
            index = input("Which index? ")
            pos = int(index)
            print("Row: {}".format(int(pos/8)))
            print("Col: {}".format(pos%8))
    elif sys.argv[1] == "p":
        print(cellPaths)
        display([str(i) for i in range(64)])
        while True:
            index = input("Which index? ")
            pos = int(index)
            print(cellPaths[pos])
