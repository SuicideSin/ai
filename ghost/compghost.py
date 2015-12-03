import sys
import termios
import contextlib
import os
import itertools

file = open('words.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))

def canForm(word):
    global words
    contains = False
    for term in words:
        if word in term:
            contains = True
    return contains
    
def best(word, options, currPlayer, playerCycle):
    goal = None
    alt = None
    loser = 0
    pos = 0
    min = 1000
    max = 0
    for option in options:
        for i in range(len(option)):
            if pos > len(playerCycle) - 1:
                pos = 0
            loser = playerCycle[pos]
            pos += 1
        if loser != currPlayer:
            #bestChars.add(option[len(word):len(word)+1])
            if len(option) < min:
                min = len(option)
                goal = option
        #allChars.add(option[len(word):len(word)+1])
        if len(option) > max:
            max = len(option)
            alt = option
    if goal is None:
        bestChar = alt[len(word):len(word)+1]
    else:
        bestChar = goal[len(word):len(word)+1]
    return bestChar

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def main():
    word = ""
    letters = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)]
    nums = [str(num) for num in range(10)]
    numPlayers = 2
    computers = []

    if len(sys.argv) > 1:
        numPlayers = int(sys.argv[1])
    if len(sys.argv) > 2:
        i = 1
        args = [sys.argv[i] for i in range(1, len(sys.argv))]
        numPlayers = len(args)
        pos = 0
        for i in args:
            if i in nums:
                pos += int(i)
            if i == 'c':
                pos += 1
                computers.append(str(pos))

    ghost = "GHOST"
    players = {str(i): 0 for i in range(1, numPlayers+1)}
    if numPlayers <= 6:
        colors = ['\033[3{}m'.format(i) for i in range(1,7)]
        playerColors = {str(i): colors[i-1] for i in range(1, numPlayers+1)}
    else:
        playerColors = {str(i): '\033[0m' for i in range(1, numPlayers+1)}
    endColor = '\033[0m'
    playerCycle = sorted([str(i) for i in range(1, numPlayers+1)])
    ejected = []
    turn = 0
    currPlayer = None
    prevPlayer = None
    winner = None
    loser = None
    responding = False
    response = ""
    print('{} Player game started.'.format(numPlayers))
    print('Terminate with ctrl+C or ctrl+D. Press 0 to reset word and ` to clear screen.')

    with raw_mode(sys.stdin):
        try:
            while True:
                '''KeyLogger Stuff'''
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break

                '''Ghost Logic'''
                
                if responding == True:
                    if ch in letters:
                        print(ch, end="",flush=True)
                        response += ch
                        continue
                    if ord(ch) == 0x7f and len(response) > 0:
                        response = response[:len(response)-1]
                        print("\b \b", end="", flush=True)
                        continue

                    if ord(ch) == 0x0a:
                        print("\n",end="")
                        if response in words and len(response) > len(word) and response[:len(word)] == word:
                            print("'{}' is valid.".format(response))
                            players[challenger] = players[challenger] + 1
                            print("{}Player {}{} loses and is now a {}{}{}.".format(playerColors[challenger], challenger, endColor, playerColors[challenger], ghost[:players[challenger]], endColor))
                            winner = currPlayer
                            loser = challenger
                        else:
                            print("'{}' is not valid.".format(response))
                            players[currPlayer] = players[currPlayer] + 1
                            print("{}Player {}{} loses and is now a {}{}{}.".format(playerColors[currPlayer], currPlayer, endColor, playerColors[currPlayer], ghost[:players[currPlayer]], endColor))
                            winner = challenger
                            loser = currPlayer
                        response = ""
                        word = ""
                        responding = False

                if ch in players:
                    challenger = ch
                    chalString = "{}Player {}{}".format(playerColors[challenger], challenger, endColor)
                    currString = "{}Player {}{}".format(playerColors[currPlayer], currPlayer, endColor)
                    if len(word) <= 3 and word in words:
                        print("Word must be longer than 3 letters in order to be challenged!")
                        continue
                    if challenger == currPlayer:
                        print("You cannot challenge yourself.")
                        continue
                    if word in words:
                        players[currPlayer] = players[currPlayer] + 1
                        print("{} challenges {}!".format(chalString, currString))
                        print("'{}' is a word.".format(word))
                        print("{} loses and is now a {}{}{}.".format(currString, playerColors[currPlayer], ghost[:players[currPlayer]], endColor))
                        winner = challenger
                        loser = currPlayer
                        word = ""
                    else:
                        print("{} challenges {}!".format(chalString, currString))
                        print("{}, please enter a word that begins with '{}': ".format(currString, word), end="",flush=True)
                        responding = True

                if loser is not None and players[loser] == len(ghost):
                    print("{}Player {}{} has been ejected!".format(playerColors[loser], loser, endColor))
                    ejected.append(loser)
                    del players[loser]
                    playerCycle = sorted([str(i) for i in range(1, numPlayers+1) if str(i) not in ejected])
                    loser = None

                if winner != None:
                    turn = playerCycle.index(winner)
                    currPlayer = playerCycle[turn]
                    turn += 1
                    winner = None
                    
                elif ch in letters:
                    if winner != None:
                        pass
                        turn = playerCycle.index(winner)
                        currPlayer = playerCycle[turn]
                        turn += 1
                        winner = None
                    else:
                        if turn > len(playerCycle) - 1:
                            turn = 0
                        currPlayer = playerCycle[turn]
                        turn += 1
                    word = ''.join([word, ch])
                    print("{}Player {}>{}{}".format(playerColors[currPlayer], currPlayer, endColor, word))

                    # #Computer checks if challenge can be made
                    # MUST FIX WHEN A COMPUTER IS A WINNER AND PLAYS NEXT, CURRENTLY THE CMOPUTER WONT PLAY!!
                    challenger = [i for i in playerCycle if i in computers][0]
                    chalString = "{}Computer {}{}".format(playerColors[challenger], challenger, endColor)
                    currString = "{}Player {}{}".format(playerColors[currPlayer], currPlayer, endColor)
                    if word in words and len(word) > 3:
                        players[currPlayer] = players[currPlayer] + 1
                        print("{} challenges {}!".format(chalString, currString))
                        print("'{}' is a word.".format(word))
                        print("{} loses and is now a {}{}{}.".format(currString, playerColors[currPlayer], ghost[:players[currPlayer]], endColor))
                        winner = challenger
                        loser = currPlayer
                        word = ""
                        continue
                    if canForm(word) is False:
                        print("{} challenges {}!".format(chalString, currString))
                        print("{}, please enter a word that begins with '{}': ".format(currString, word), end="",flush=True)
                        responding = True
                        continue

                    #COMPUTER'S TURN!!!!
                    nextTurn = turn
                    if nextTurn> len(playerCycle) - 1:
                        nextTurn = 0
                    nextPlayer = playerCycle[nextTurn]
                    
                    if nextPlayer in computers:
                        if turn > len(playerCycle) - 1:
                            turn = 0
                        prevPlayer = currPlayer
                        currPlayer = playerCycle[turn]
                        turn += 1
                        
                        if word == "":
                            bestChar = best(word, words, currPlayer, playerCycle)
                        else:
                            options = []
                            for i in words:
                                if word != i and word == i[:len(word)]:
                                    if i[:len(word)+1] not in words: #smart guess
                                        options.append(i)
                            if len(options) == 0:
                                #print("<INSERT CHALLENGE (LAST RESORT)>")
                                challenger = currPlayer
                                currPlayer = prevPlayer
                                chalString = "{}Computer {}{}".format(playerColors[challenger], challenger, endColor)
                                currString = "{}Player {}{}".format(playerColors[currPlayer], currPlayer, endColor)
                                print("{} challenges {}!".format(chalString, currString))
                                print("{}, please enter a word that begins with '{}': ".format(currString, word), end="",flush=True)
                                responding = True
                                continue
                            
                            bestChar = best(word, options, currPlayer, playerCycle)

                        word = ''.join([word, bestChar])
                        print("{}Computer {}>{}{}".format(playerColors[currPlayer], currPlayer, endColor, word))




                elif ch == ".":
                    options = []
                    hints = set()
                    for term in words:
                        if word != term and word == term[:len(word)]:
                            #if term[:len(word)+1] not in words: #smart hint
                            options.append(term)
                    for option in options:
                        hints.add(option[len(word):len(word)+1])
                    if len(hints) == 0:
                        print("No hints! Starting new word.")
                        word = ""
                    else:
                        print("H>{}".format(word+"."))
                        print("Hints: {}".format(hints))


                elif ch == "0":
                    word = ""
                    ejected = []
                    playerCycle = sorted([str(i) for i in range(1, numPlayers+1) if i not in ejected])
                    print("Word reset.")
                elif ch== "`":
                    os.system('cls' if os.name == 'nt' else 'clear')

                if len(players) == 1:
                    for player in players:
                        assert player not in ejected
                        print("{}Player {}{} wins!".format(playerColors[player], player, endColor))
                        sys.exit()



        except (KeyboardInterrupt, EOFError):
            print("Game Terminated.")
            pass

if len(sys.argv) > 1:
    main()
else:
    import ghost
    ghost.main()
