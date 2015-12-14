import sys
import termios
import contextlib
import os

file = open('words.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))

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

def challenge()
    return winner
    
def turn()
    return char

def computer()
    return char

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
