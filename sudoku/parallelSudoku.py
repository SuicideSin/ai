import sys, time, queue
from multiprocessing import Pool

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

def stringBoard(puzzle):
    string = ""
    if puzzle == "":
        return
    i = 1
    x = 0
    c = 0
    string += ",,,,,,,,,,,,,,,,,,,\n"
    for char in puzzle:
        r = int(i/9)
        c += 1
        if c == 1:
            string += "|"

        string += char

        if c%3 != 0:
            string += " "


        if c%3 == 0 and x<2:
            x += 1
            string += "|"

        if c==9:
            string += "|"

        if i%9 == 0:
            c = 0
            x = 0
            if int(i/9)%3==0 and r<9:
                string += "\n|-----+-----+-----|\n"
            else:
                string += "\n"

        i += 1
    string += "```````````````````\n"

    return string

def validateUnit(unit):
    # if len(unit) != 9:
    #     return False
    # if '.' in unit:
    #     return False
    # for num in "123456789":
    #     if num not in unit:
    #         return False

    temp = ""
    for num in unit:
        if num not in "123456789.":
            return False
        if num != '.':
            temp += num
    if len(temp)!=len(set(temp)):
        return False
    return True



def validateSudoku(puzzle):
    dic = {}
    cols = {}
    boxes = {}

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
        b = str(rsec) + str(csec)
        if b not in boxes:
            boxes[b] = []
        boxes[b].append(char)
        i += 1

    for r in range(0,9):
        for c in range(0,9):
            char = dic[r][c]

            #if char != '.' or char == '.':
            r = r
            c = c
            rsec = int(r/3)
            csec = int(c/3)
            b = str(rsec) + str(csec)

            row = dic[r]
            col = cols[c]
            box = boxes[b]

            if not (validateUnit(col) and validateUnit(row) and validateUnit(box)):
                return False
    return True

file = open('sudoku.txt', 'r')

sudoku = {}
i = 0
for line in file:
    sudoku[i] = line.rstrip('\n')
    i += 1

puzzle = sudoku[0]

file = open("parallel.txt", 'w')

def solve(start, end):
    tuples = []

    for i in range(start, end):
        puzzle = sudoku[i]
        count = i+1
        string = ""

        start = time.clock()
        puzzle = bruteForce(puzzle)
        delta = time.clock() - start

        string += "Puzzle " + str(count) + "\n"
        string += stringBoard(puzzle)
        if(delta >= 60):
            string += "Puzzle {} completed in {} minutes and {} seconds.\n".format(count, int(delta/60), delta%60)
        else:
            string += "Puzzle {} completed in {} seconds.\n".format(count, delta)
        string += "===============================================================\n\n"

        tuple = (i, string)
        tuples.append(tuple)

    return tuples



if len(sys.argv) == 1:

    pool = Pool()
    r1 = pool.apply_async(solve, [0, 16])
    r2 = pool.apply_async(solve, [16, 32])
    r3 = pool.apply_async(solve, [32, 48])
    r4 = pool.apply_async(solve, [48, 64])
    r5 = pool.apply_async(solve, [64, 80])
    r6 = pool.apply_async(solve, [80, 96])
    r7 = pool.apply_async(solve, [96, 112])
    r8 = pool.apply_async(solve, [112, 128])

    a1 = r1.get(timeout=10000)
    a2 = r2.get(timeout=10000)
    a3 = r3.get(timeout=100000)
    a4 = r4.get(timeout=100000)
    a5 = r5.get(timeout=1000000)
    a6 = r6.get(timeout=1000000)
    a7 = r7.get(timeout=10000000)
    a8 = r8.get(timeout=10000000)

    # r1 = pool.apply_async(solve, [0, 2])
    # r2 = pool.apply_async(solve, [2, 4])
    # r3 = pool.apply_async(solve, [4, 6])
    # r4 = pool.apply_async(solve, [6, 8])
    # r5 = pool.apply_async(solve, [8, 10])
    # r6 = pool.apply_async(solve, [10, 12])
    # r7 = pool.apply_async(solve, [12, 14])
    # r8 = pool.apply_async(solve, [14, 16])
    #
    # a1 = r1.get(timeout=10000)
    # a2 = r2.get(timeout=10000)
    # a3 = r3.get(timeout=100000)
    # a4 = r4.get(timeout=100000)
    # a5 = r5.get(timeout=1000000)
    # a6 = r6.get(timeout=1000000)
    # a7 = r7.get(timeout=10000000)
    # a8 = r8.get(timeout=10000000)

    array = a1 + a2 + a3 + a4 + a5 + a6+ a7+ a8

    q = queue.PriorityQueue()

    for tuple in array:
        q.put(tuple)

    while q:
        print(q.get()[1])

    #
    # print(q.get())
    # print(q.get())







#end of file
