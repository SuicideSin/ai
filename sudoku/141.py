import sys, time

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

allGroups = [[pos for pos in range(row, row+9)] for row in range(0, 81, 9)] + [[pos for pos in range(col, 81, 9)] for col in range(9)] + allBoxes

allSyms = {str(i) for i in range(1, 10)}
cellNeighbors = [set().union(*[grp for grp in allGroups if pos in grp]) - {pos} for pos in range(0, 81)]
guesses = 0

def findPossible(puzzle):
    allPossible = {i : allSyms - {puzzle[ps] for ps in cellNeighbors[i] if puzzle[ps] != '.'} for i in range(0, 81)}
    return {i : allPossible[i] for i in allPossible if puzzle[i] not in allPossible[i]}

def makeDeductions(puzzle):
    global cellNeighbors, allGroups
    possible = findPossible(puzzle)

    for i in possible:

        if puzzle[i] == ".":
            if len(possible[i]) == 0:
                return ""
                
            '''If only one value is not excluded from being in a box, then the value must go in that box'''
            if len(possible[i]) == 1:
                for char in possible[i]:
                    for pos in cellNeighbors[i]:
                        if pos in possible:
                            if char in possible[pos]:
                                possible[pos].remove(char)
                    puzzle = puzzle[:i] + char + puzzle[i+1:]

    '''If in a group there are K cells that have only the same K possiblities, then those K possibilities can be excluded from all other cells'''

    for grp in allGroups:
        subsets = {pos: possible[pos] for pos in grp if pos in possible}
        array = list(subsets.values())
        for pos in subsets:
            if len(subsets[pos]) == array.count(subsets[pos]):
                for j in subsets:
                    if subsets[pos] != subsets[j]:
                        for char in subsets[pos]:
                            if char in possible[j]:
                                possible[j].remove(char)

    return (puzzle, possible)

def bruteForce(puzzle):

    global guesses, allGroups, cellNeighbors
    guesses += 1

    tpl = makeDeductions(puzzle)
    if tpl == "":
        return ""
    puzzle, possible = tpl

    pos = puzzle.find('.')
    if pos < 0:
        return puzzle

    
    min = 10
    for i in possible:
        if puzzle[i] == ".":
            s = len(possible[i])
            if s < min:
                min = s
                pos = i

    for char in possible[pos]:
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

file = open('sudoku141.txt', 'r')

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
    possible = findPossible(puzzle)

    solved = bruteForce(puzzle)

    showBoard(solved)
    delta = time.clock() - start
    if(delta >= 60):
        print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
    else:
        print("Puzzle {} completed in {} seconds.".format(count, delta))
    print()
    print("\n")

if len(sys.argv) == 1:
    fout = open("valid.txt", "w")
    total = 0
    for i in sudoku:
        count = i+1
        puzzle = sudoku[i]

        start = time.clock()
        possible = findPossible(puzzle)
        solved = bruteForce(puzzle)

        #print("Puzzle {}".format(count))
        #showBoard(puzzle)

        delta = time.clock() - start
        if(delta >= 60):
            print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
        else:
            print("Puzzle {} completed in {} seconds.".format(count, delta))
        print(puzzle)
        print(solved)
        total += delta

        print("\n")
        fout.write(solved + "\n")

if len(sys.argv) == 3:
    total = 0
    for i in range(int(sys.argv[1]), int(sys.argv[2])+1):
        count = i
        puzzle = sudoku[i-1]

        start = time.clock()
        possible = findPossible(puzzle)
        solved = bruteForce(puzzle)


        delta = time.clock() - start
        if(delta >= 60):
            print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
        else:
            print("Puzzle {} completed in {} seconds.".format(count, delta))
        print(puzzle)
        print(solved)
        total += delta
        print("\n")

if len(sys.argv) != 2:
    print("Total time elapsed: {} seconds".format(total))
print("{} guesses.".format(guesses))








#end of file
