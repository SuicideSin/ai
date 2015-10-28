import sys, time, pickle, queue

allGroups = [ [] for i in range(9)]

for i in range(0, 81):
    c = i%9
    if allGroups[c] == None:
        allGroups[c] = []
    allGroups[c].append(i)

allSyms = set(i for i in range(1, 10))

cellNeighbors = [ set() for i in range(0, 81) ]
for i in range(0, 81):
    for j in range(1, 9):
        cellNeighbors[i].add(i+j*9)

def findPossible(puzzle):
    dic = {}
    for i in range(0, 81):
        dic[i] = allSyms - {puzzle[ps] for ps in cellNeighbors[pos] if puzzle[ps] != '.'}

# def bruteForce(puzzle):
#
#     if not validate(puzzle):
#         return ""
#     pos = puzzle.find('.')
#     if pos < 0:
#         return puzzle
#     for char in "123456789":
#         bf = bruteForce(puzzle[:pos] + char + puzzle[pos+1:])
#         if bf != "":
#             return bf
#     return ""


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




# def validate(puzzle):
#     global aGroups
#     for groupToCheck in aGroups:
#         alreadyThere = set()
#         for pos in groupToCheck:
#             if puzzle[pos] in alreadyThere:
#                 return False
#             else:
#                 alreadyThere.add(puzzle[pos])



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
    #puzzle = bruteForce(puzzle)

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
    print(allGroups)
    print(allSyms)
    print(cellNeighbors[1])











#end of file
