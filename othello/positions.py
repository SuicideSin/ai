import sys

cellNeighbors = {i: {j for j in range(64) if j!=i and (abs(int(j/8)-int(i/8)) <= 1 and abs((j%8)-(i%8)) <= 1) } for i in range(64)}

cellStraights = {i: {j for j in range(64) if j!=i and (int(j/8)==int(i/8) or (j%8)==(i%8) or ((abs(int(j/8)-int(i/8)) == abs((j%8)-(i%8)))))} for i in range(64)}

opposite = {"X": "O", "O":"X"}

def display():
    border = ["-" for i in range(32)]
    border = "   {}".format("".join(border))
    print(border)
    for i in range(8):
        #row = [str(j+8*i) for j in range(8)]
        row = []
        for j in range(8):
            num = str(j+8*i)
            if len(num) == 2:
                row.append(num)
            else:
                row.append(num + " ")
        row = "{} | {} | {}".format(i, "  ".join(row).upper(), i)
        print(row)
    print(border)
    cols = [str(i) for i in range(8)]
    cols = "{}  {}".format("  ", "   ".join(cols))
    print(cols)
    
display()

if len(sys.argv) > 1:
    if sys.argv[1] == "n":
        print(cellNeighbors)
        print(type(cellNeighbors['0'].pop()))
    elif sys.argv[1] == "s":
        print(cellStraights)
        print(type(cellStraights['0'].pop()))
    elif sys.argv[1] == "o":
        print(opposite)
    elif sys.argv[1] == "f":
        while True:
            board = "".join([str(i) for i in range(64)])
            index = input("Which index? ")
            pos = int(index)
            print("Row: {}".format(int(pos/8)))
            print("Col: {}".format(pos%8))
    
    