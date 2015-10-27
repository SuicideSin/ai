import sys, time, pickle, queue

dic = {}

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

    for r in dic:
        x = 0

    return True

def toDictionary(puzzle):
    dic = {}
    # boxes = {}

    # val = []

    i = 0
    for char in puzzle:
        r = int(i/9)
        c = i%9
        rsec = int(r/3)
        csec = int(c/3)
        b = "".join([str(rsec), str(csec)])

        if r not in dic:
            dic[r] = {}

        if c not in dic[r]:
            dic[r][c] = {}

        if dic[r][c] == None:
            dic[r][c] = {}
        dic[r][c]['val'] = char
        dic[r][c]['box'] = b

        if b not in dic:
            dic[b] = set()
        dic[b].add(char)

        i += 1
    print(dic)
    # val.append(dic)
    # val.append(boxes)

    return dic


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

    puzzle = sudoku[i]

    dic = toDictionary(puzzle)

    print(dic)
















#end of file
