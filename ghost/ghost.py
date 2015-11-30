import sys

file = open('words.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))

import termios
import contextlib
import os
import itertools


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
    if len(sys.argv) > 1:
        numPlayers = int(sys.argv[1])
    ghost = "GHOST"
    players = {str(i): 0 for i in range(1, numPlayers+1)}
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
                    if ord(ch) == 0x7f:
                        response = response[:len(response)-1]
                        print("\b \b", end="", flush=True)
                        continue
                        
                    if ord(ch) == 0x0a:
                        print("\n",end="")
                        if response in words and len(response) > len(word) and response[:len(word)] == word:
                            print("'{}' is valid.".format(response))
                            players[challenger] = players[challenger] + 1
                            print("Player {} loses and is now a {}.".format(challenger, ghost[:players[challenger]]))
                            winner = currPlayer
                            loser = challenger
                        else:
                            print("'{}' is not valid.".format(response))
                            players[currPlayer] = players[currPlayer] + 1
                            print("Player {} loses and is now a {}.".format(currPlayer, ghost[:players[currPlayer]]))
                            winner = challenger
                            loser = currPlayer
                        response = ""
                        word = ""
                        responding = False

                if ch in players:
                    challenger = ch
                    if len(word) <= 3 and word in words:
                        print("Word must be longer than 3 letters in order to be challenged!")
                        continue
                    if challenger == currPlayer:
                        print("You cannot challenge yourself.")
                        continue
                    if word in words:
                        players[currPlayer] = players[currPlayer] + 1
                        print("Player {} challenges Player {}!".format(challenger, currPlayer))
                        print("'{}' is a word.".format(word))
                        print("Player {} loses and is now a {}.".format(currPlayer, ghost[:players[currPlayer]]))
                        winner = challenger
                        loser = currPlayer
                        word = ""
                    else:
                        print("Player {} challenges Player {}!".format(challenger, currPlayer))
                        print("Player {}, please enter a word that begins with '{}': ".format(currPlayer, word), end="",flush=True)
                        responding = True

                if loser is not None and players[loser] == len(ghost):
                    print("Player {} has been ejected!".format(loser))
                    ejected.append(loser)
                    del players[loser]
                    playerCycle = sorted([str(i) for i in range(1, numPlayers+1) if str(i) not in ejected])
                    loser = None


                elif ch in letters:
                    if winner != None:
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
                    print("P{}>{}".format(currPlayer, word))

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
                        print("Player {} wins!".format(player))
                        sys.exit()



        except (KeyboardInterrupt, EOFError):
            print("Game Terminated.")
            pass


main()
