import sys, time, pickle, queue

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


file = open('lol.txt', 'r')

sudoku = {}
i = 0
for line in file:
    sudoku[i] = line.rstrip('\n')
    i += 1

for i in sudoku:
    print(validateSudoku(sudoku[i]))
