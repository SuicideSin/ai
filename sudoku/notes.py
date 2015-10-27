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

        if two ipnuts are equal:
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


aGroups = [[0, 9, 18, 27, ..., 72], ... ]



'''
List Comprehensions:
'''
aList = [ i for i in range(9) ]

aList = [ i for i in range(100) if i % 2 == 0 ]

# aList = [ for i in ra ]



















#
