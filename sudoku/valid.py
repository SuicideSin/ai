import sys, time

allRows = [[pos for pos in range(row, row+9)] for row in range(0, 81, 9)]
allCols = [[pos for pos in range(col, 81, 9)] for col in range(9)]

boxes = {}
for i in range(0, 81):
    r = int(i/9)
    c = i%9
    rsec = int(r/3)
    csec = int(c/3)
    b = "".join([str(rsec), str(csec)])
    if b not in boxes:
        boxes[b] = []
    boxes[b].append(i)
allBoxes = [boxes[box] for box in boxes]

allGroups = allRows + allCols + allBoxes


def validate(puzzle):
    global allGroups
    for groupToCheck in allGroups:
        alreadyThere = set()
        for pos in groupToCheck:
            if puzzle[pos] in alreadyThere:
                return False
            else:
                if puzzle[pos] != '.':
                    alreadyThere.add(puzzle[pos])
    return True


file = open('test.txt', 'r')

sudoku = {}
i = 0
for line in file:
    sudoku[i] = line.rstrip('\n')
    i += 1

for i in sudoku:
    print(validate(sudoku[i]))
