'''
1. code will accept one arg, the line number of the puzzle
if no arg given, solve all of the puzzles


2. write showBoard(puzzle)
    prints puzzle

3. write validateSudoku(puzzle)
    returns False if puzzle is invalid
    returns True otherwise
'''

def bruteForce(puzzle):
    if not validateSudoku(puzzle):
        return ""
    pos = puzzle.find('.')
    if pos < 0:
        return puzzle
    for char in "123456789":
        bf = bruteForce(puzzle[:pos] + c + puzzle[pos+1:])
        if bf != "":
            return bf
    return ""



'''


3 possiblities for inputs:

    - no inputs
        solve all of the puzzles
    - one input
        solve specific puzzle
    - two inputs
        solve range of puzzles

        if first and last ipnuts are equal:
            print the starting puzzle, starting board, and ending board
'''





'''
validateSudoku speedup:

create a global variable (aGroups) --compute all positions ONLY ONCE
    30% \faster

bruteforce speedup:
 - don't test all possible values thta can go into a position, only do the ones that aren't already in a group
    does not result in that large of a speedup

 - choose the cell that has the largest chance of success:
    DO IT


'''


aGroups = [[0, 9, 18, 27, ..., 72],  ... ]  #ALL GROUPS (rows, cols, boxes)


'''
But how do we use aGroups???
'''
def validate(puzzle):
    global aGroups
    for groupToCheck in aGroups:
        alreadyThere = set()
        for pos in groupToCheck:
            if puzzle[pos] in alreadyThere:
                return False
            else:
                alreadyThere.add(puzzle[pos])

'''
ASSIGNMENT for 11/3/15:
'''

''' 1. create global set of all symbols only needs to be computed once'''
    allSyms = {i for i in range(9)}

''' 2. Create a list called cellNeighbors, which is a list where the index is the position of a cell and the value is a set of the positions of all the neighbors of that cell (20 neighbors per cell) (maybe use aGroups to compute it). only needs to be computed once '''
    cellNeighbors[1] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 27, 36, 45, 56, 72, 10, 11, 19, 20}

''' 3. Create findPossible(puzzle), which is a function that returns a dictionarywhere the keys are the positions of the cells in puzzle that are unset, and the values of set of symbols that could fill that cell. must be computed for every puzzle'''
    allSyms - {puzzle[ps] for ps in cellNeighbors[pos] if puzzle[ps] != '.'}

''' end '''

'''
List Comprehensions:
'''
aList = [ i for i in range(9) ]

aList = [ i for i in range(100) if i % 2 == 0 ]

# aList = [ for i in ra ]



'''
important array stuff
'''

foo = [1,2,3]
bar = foo[:] '''COPIES THE LIST'''
bar = foo '''POINTS TO THE LIST, changes to bar will affect foo'''

mySet = {1,2,3,4}
myCopiedSet = mySet + set()

'''
Pythonic allGroups construction

aRow = list of lists of positions
aCol = list of lists of positions
aBox = list of lists of positions
'''

aRow = [[ startPos + offSet for offset in range(9)  ] for startPos in range(0, 81, 9)  ]

'''
Pythonic cellNeighbors construction
'''

cellNeighbors = [set() for dummy range(0, 81)]
for grp in aGroups:
    for pos1 in grp:
        cellNeighbors[pos1] |= (grp - {pos1})

cellNeighbors = [set().union(*[grp for grp in aGroups if pos in grp]) - {pos} for pos in range(0, 81)]

''''
Operations on hashes on a per element basis is basically constant, because elements in sets are hashed


Pythonic Validation
''''


'''
Create unGroup, which is a list where the index indicates the group number and the entry is the set of all position in that group that are not set
'''



def bf(puzzle):
    puzzle, possible = makeDeductions(puzzle)

    find cell with '.'

    for each possible char @ the position
        pzl = bf(puzzle with char stuffed in)
        if pzl != "": return pzl

    return puzzle


def makeDeductions(puzzle):
    possible = findPossible(puzzle)
    
    while deductions can be made:
        make a dedcution =>
            update puzzle
            update possible
    return (puzzle, possible)

''' Deductions
1. If only one value is not excluded from being in a box, then the value must go in that box
2. If there is only one box where a value is not excluded from in a unit, then the value must go there.
3. If in a group there are K cells that have only the same K possiblities, then those K possibilities can be excluded from all other cells


- if 0 possibilities, puzzle is invalid, return ""
- If there is an entry with only 2 possible locations in possible dictionaries, choose one of those positions

[(pos1, sym1), (pos2, sym1), (pos1, sym2)]

'''





#
