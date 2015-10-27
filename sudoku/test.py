import sys, time, pickle, queue

aGroups = []
for i in range(0, 9):
    aGroups.append([])

def bruteForce(puzzle):

    if not validateSudoku(puzzle):
        return ""
    pos = puzzle.find('.')
    if pos < 0:
        return puzzle
    for char in "123456789":
        bf = bruteForce(puzzle[:pos] + char + puzzle[pos+1:])
        if bf != "":
            return bf
    return ""


def showBoard(puzzle):
    if puzzle == "":
        return
    i = 1
    x = 0
    c = 0
    print(",,,,,,,,,,,,,,,,,,,")
    for char in puzzle:
        r = int(i/9)
        c += 1
        if c == 1:
            print("|", end="")

        print("{}".format(char), end="")

        if c%3 != 0:
            print(" ", end="")


        if c%3 == 0 and x<2:
            x += 1
            print("|", end="")

        if c==9:
            print("|", end="")

        if i%9 == 0:
            c = 0
            x = 0
            if int(i/9)%3==0 and r<9:
                print("\n|-----+-----+-----|")
            else:
                print()

        i += 1
    print("```````````````````")

def validateUnit(unit):
    temp = ""
    for num in unit:
        if num not in "123456789.":
            return False
        if num != '.':
            temp = "".join([temp, num])

    if len(temp)!=len(set(temp)):
        return False
    return True

def validateSudoku(puzzle):
    dic = {}
    cols = {}
    boxes = {}
    visited = {}

    i = 0
    for char in puzzle:
        r = int(i/9)
        if r not in dic:
            dic[r] = []
        dic[r].append(char)

        c = i%9
        if c not in cols:
            cols[c] = []
        cols[c].append(char)

        rsec = int(r/3)
        csec = int(c/3)
        b = "".join([str(rsec), str(csec)])
        if b not in boxes:
            boxes[b] = []
        boxes[b].append(char)
        i += 1

    for r in dic:
        rname = "".join(["r", str(r)])
        bool = validateUnit(dic[r])
        if bool == False:
            return False
        visited[rname] = bool

    for c in cols:
        cname = "".join(["c", str(c)])
        bool = validateUnit(cols[c])
        if bool == False:
            return False
        visited[cname] = bool

    for b in boxes:
        bool = validateUnit(boxes[b])
        if bool == False:
            return False
        visited[b] = bool

    return True


def toArray(puzzle):
    for i in range(0, 81):
        c = i%9
        if aGroups[c] == None:
            aGroups[c] = []
        aGroups[c].append(i)


file = open('sudoku.txt', 'r')

sudoku = {}
i = 0
for line in file:
    sudoku[i] = line.rstrip('\n')
    i += 1

puzzle = sudoku[0]

if len(sys.argv) == 2:
    count = int(sys.argv[1])
    i = count - 1
    print(sudoku[i])

    puzzle = sudoku[i]
    showBoard(puzzle)
    start = time.clock()
    puzzle = bruteForce(puzzle)

    #print("Puzzle {}".format(count))

    showBoard(puzzle)
    delta = time.clock() - start
    if(delta >= 60):
        print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
    else:
        print("Puzzle {} completed in {} seconds.".format(count, delta))
    print()
    #print(puzzle)
    print("\n")
    toArray(puzzle)
    print(aGroups)

file = open("test.txt", 'w')

if len(sys.argv) == 1:
    for i in sudoku:
        count = i+1
        puzzle = sudoku[i]

        start = time.clock()
        puzzle = bruteForce(puzzle)

        #print("Puzzle {}".format(count))
        #showBoard(puzzle)
        #print(puzzle)
        delta = time.clock() - start
        if(delta >= 60):
            print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
        else:
            print("Puzzle {} completed in {} seconds.".format(count, delta))
        print(puzzle)
        print("\n")
        toArray(puzzle)
        print(aGroups)

        #file.write("Puzzle " + str(count) + "\n")
        #file.write(stringBoard(puzzle))
        if(delta >= 60):
            file.write("Puzzle {} completed in {} minutes and {} seconds.\n".format(count, int(delta/60), delta%60))
        else:
            file.write("Puzzle {} completed in {} seconds.\n".format(count, delta))
        file.write(puzzle)
        file.write("\n\n")

if len(sys.argv) == 3:
    if int(sys.argv[1]) == int(sys.argv[2]):
        count = int(sys.argv[1])
        i = count - 1
        print(sudoku[i])

        puzzle = sudoku[i]
        showBoard(puzzle)
        start = time.clock()
        puzzle = bruteForce(puzzle)

        #print("Puzzle {}".format(count))

        showBoard(puzzle)
        delta = time.clock() - start
        if(delta >= 60):
            print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
        else:
            print("Puzzle {} completed in {} seconds.".format(count, delta))
        print()
        #print(puzzle)
        print("\n")
    else:
        for count in range(int(sys.argv[1]), int(sys.argv[2])+1):
            i = count - 1
            puzzle = sudoku[i]

            start = time.clock()
            puzzle = bruteForce(puzzle)

            #print("Puzzle {}".format(count))
            #showBoard(puzzle)
            #print(puzzle)
            delta = time.clock() - start
            if(delta >= 60):
                print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
            else:
                print("Puzzle {} completed in {} seconds.".format(count, delta))
            print(puzzle)
            print("\n")














#end of file
