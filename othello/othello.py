import sys





if len(sys.argv) > 1:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1]
        border = ["-" for i in range(24)]
        border = " ".join(border)
        print(border)
        for i in range(7):
            row = [board[j+j*i] for j in range(8)]
            row = "{} | {}".format(i,"  ".join(row))
            print(row)
