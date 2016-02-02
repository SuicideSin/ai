import sys, time, math, random

if len(sys.argv)>1:
  board = sys.argv[1].upper()
  for theBlank in board:
    if theBlank!="X" and theBlank!="O": break
  if theBlank=="X" or theBlank=="O":
    print ("Game is already over")
    exit()
else:
  theBlank = "."
  board = (theBlank*(3*8+3)) + "OX" + theBlank*6 + "XO" + (theBlank*(3*8+3))
token = sys.argv[2].upper() if len(sys.argv)>2 else ("O" if board.count(theBlank) % 2 else "X")

# print ("boardLen: {}".format(len(board)))

# To do:
# Done: Debug Stop if strategy returns illegal move
# Done: debug (Why are we returning 64 sometimes)
# Done: debug (Random move currently printing extra stuff)
# Done: Accept file names as input arguments
# Done: Return output from playGame
# Done: Accumulate extra time
# Done: Run multiple times
# Done: Quiet the output
# Done: Print summary score when there are multiple runs
# 1. If only playing one game, should print game info

# 2. Pick the move maximizing resulting points (ie greatest number of flips)
# 3. If we can play into a corner, do so
# 4. Pick a move maximizing the number of move possibilities

# if we can play onto an edge without corners where we can't be captured, then do so
# Improve neighbors of blank cells for finding moves
# if our play allows opponent to take a corner, avoid it
# pick a move minimizing the number of move possibilities for the opponent
# pick a move maximizing the number of move possibilities after an even number of moves

def defineNeighbors(bL):
  # bL = the board length
  b2 = bL*bL
  
  aNeigh = [{p+1, p-1, p+bL, p-bL, p+bL-1, p+bL+1, p-bL-1, p-bL+1} for p in range(b2)]

  # Adjust edges:
  for p in range(0, bL): aNeigh[p] -= {p-bL-1, p-bL, p-bL+1}
  for p in range(0, b2, bL): aNeigh[p] -= {p-1, p-bL-1, p+bL-1}
  for p in range(bL-1, b2, bL): aNeigh[p] -= {p+1, p+bL+1, p-bL+1}
  for p in range(b2-bL, b2): aNeigh[p] -= {p+bL-1, p+bL, p+bL+1}

  # Adjust corners (should be redundant):
  aNeigh[0] = {1, bL, bL+1}
  aNeigh[bL-1] = {bL-2, 2*bL-1, 2*bL-2}
  aNeigh[b2-1] = {b2-2, b2-bL-1, b2-bL-2}
  aNeigh[b2-bL] = {b2-bL+1, b2-2*bL, b2-2*bL+1}

  enemyCheck = [aNeigh[p].copy() for p in range(b2)]
  for p in range(0, bL): enemyCheck[p] -= {p-1, p+1}
  for p in range(0, b2, bL): enemyCheck[p] -= {p-bL, p+bL}
  for p in range(bL-1, b2, bL): enemyCheck[p] -= {p-bL, p+bL}
  for p in range(b2-bL, b2): enemyCheck[p] -= {p-1, p+1}
  # Adjust corners (not redundant)
  for p in {0, bL-1, b2-1, b2-bL}: enemyCheck = set()

  return aNeigh, enemyCheck

def findMoves(board, token, aNeigh):
#  print ("boardLen: {}".format(len(board)))
  b2 = len(board)
  enemy = "X" if token=="O" else "O"
  setMoves = set()
  for p in range(b2):
    if board[p]!=theBlank: continue
#    print ("findMoves index: {}".format(p))
    moveFound = False
    for np in aNeigh[p]:                   # should be improved
#      print ("findMoves neighbor: {}".format(np))
      if board[np]!=enemy: continue
      diff = np-p
      while np+diff in aNeigh[np]:
        np += diff
        if board[np]!=enemy:
          moveFound = (board[np]==token)
          break
      if moveFound:
        setMoves.add(p)
        break
  return setMoves    


'''
def defineNeighbors(bL):
  # bL = the board length
  b2 = bL * bL
  # inner portion
  dctNeighbors = {rowBase + col: {rb+cl for rb in {rb-bL, rb, rb+bL} for cl in {col-1, col, col+1}} - {rowBase+col} \
                  for rowBase in range(bL, b2-bL, bL) \
                  for col in range(1,bL-1)}
  # Corners
  dctNeighbors[0] = {1, bL, bL+1}
  dctNeighbors[bL-1] = {bL-2, 2*bL-1, 2*bL-2}
  dctNeighbors[b2-1] = {b2-2, b2-bL-1, b2-bL-2}
  dctNeighbors[b2-bL] = {b2-bL+1, b2-2*bL, b2-2*bL+1}

  # Edges
  for idx in range(1, bL-1): dctNeighbors[idx] = {idx-1, idx+1, idx+bL-1, idx+bL, idx+bL+1}
  for idx in range(b2-bL+1, b2-1): dctNeighbors[idx] = {idx-1, idx+1, idx-bL-1, idx-bL, idx-bL+1}
  for idx in range(bL,b2-bL,bL): dctNeighbors[idx] = {idx+1, idx-bL, idx-bL+1, idx+bL, idx+bL+1}
  for idx in range(2*bL-1,b2-bL-1,bL): dctNeighbors[idx] = {idx-1, idx-bL, idx-bL-1, idx+bL, idx+bL-1}

  return dctNeighbors
'''

aNeigh, enemyCheck = defineNeighbors(int(math.sqrt(len(board))))

# print aNeigh

setMoves = findMoves (board, token, aNeigh)

# print setMoves

if len(setMoves)==0: print ("P"); exit()
print ("{}".format(random.sample(list(setMoves),1)[0]))
#print ("{}".format(setMoves.pop()))

