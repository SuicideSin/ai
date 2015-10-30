import sys, time, pickle, queue
from multiprocessing import Pool

list = pickle.load( open( 'sets.pkl' , 'rb' ) )

allGroups = list[0]
allSyms = set(str(i) for i in range(1, 10))
cellNeighbors = list[1]
possible = {}
guesses = 0

def findPossible(puzzle):
    dic = {}
    for i in range(0, 81):
        if puzzle[i] == '.':
            dic[i] = allSyms - {puzzle[ps] for ps in cellNeighbors[i] if puzzle[ps] != '.'}
    return dic

def bruteForce(puzzle):

    global possible, guesses
    guesses += 1

    if not validate(puzzle):
        return ""
    pos = puzzle.find('.')
    if pos < 0:
        return puzzle

    min = 10
    for i in possible:
        s = len(possible[i])
        if s < min and puzzle[i]==".":
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

def validatePart(puzzle, start, end):
    global allGroups
    for i in range(start, end):
        grouptoCheck = allGroups[i]
        alreadyThere = set()
        for pos in groupToCheck:
            if puzzle[pos] in alreadyThere:
                return False
            else:
                if puzzle[pos] != '.':
                    alreadyThere.add(puzzle[pos])
    return True

def validate(puzzle):
    pool = Pool()
    r1 = pool.apply_async(validate, [puzzle, 0, 7])
    r2 = pool.apply_async(validate, [puzzle, 7, 14])
    r3 = pool.apply_async(validate, [puzzle, 14, 21])
    r4 = pool.apply_async(validate, [puzzle, 21, 27])

    a1 = r1.get(timeout=10)
    a2 = r2.get(timeout=10)
    a3 = r3.get(timeout=10)
    a4 = r4.get(timeout=10)

    if a1 or a2 or a3 or a4 == False:
        return False
    return True


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
    possible = findPossible(puzzle)

    solved = bruteForce(puzzle)

    showBoard(solved)
    delta = time.clock() - start
    if(delta >= 60):
        print("Puzzle {} completed in {} minutes and {} seconds.".format(count, int(delta/60), delta%60))
    else:
        print("Puzzle {} completed in {} seconds.".format(count, delta))
    print()
    #print(solved)
    print("\n")

if len(sys.argv) == 1:
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

        if count == 51:
            if len(sys.argv) != 2:
                print("\nTotal time elapsed: {} seconds".format(total))
            print("{} guesses.".format(guesses))

        print("\n")

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
