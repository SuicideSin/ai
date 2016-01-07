'''
Othello boards are 8x8 grids

X = black
O = white

black goes first.

Specs:

Othello Program

Input schemes:
    If "othello", you vs computer

    If "othello 2", then its you vs friend

    If "othello board", then print out a board

    If "othello x (or o)", then print move
        A move is an index on the string for which the program will place an object
        The moderator will take the last printed move as the move (so that you can use as much time as you can)
            Othello is not a solved program, no program can play othello perfectly
        Printing a "P" means pass.

Competition:
Given an othello board and a color, make a move





An othello board ia  64 character sitnrg made of x's and o's and .'s for empty positions.




For Tuesday (12/15) implement board printout
For Thurday (12/17) 
    make a global dictionary which given a board index, will return the set of neighbor positions
    Given a board and character, print out the possible moves



For Tuesday of next year
1. Have a moderator for 2 person othello game
    - Start with xo board
                 ox 
    - Should accept moves in the "row col" format (comma can be placed but doesnt have to be)
    - Should display resultant board with flipped pieces
    - when both players must pass, moderator ends game and calculates winner
    - Moderator should determine if player must pass. If player passes, moderator displays a            message.
2. Allow a human vs computer game
3. Mystery assignment
4. Computer vs. Self
5. Build in smarts




For the contest, you get half a second to a second to move. Excess time can be put forward into the next move.

Entering an illegal move will carry a half point or point deduction.

400 MB limit -- TRANSPOSITION TABLES!


Ideas for computer:
    - Zobrist hashing
    - Transposition tables (400 MB, that's a lot!)
    - Implement mtd-f search
    - 

'''


