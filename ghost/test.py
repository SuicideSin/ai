
# this solution will work only in Windows, as msvcrt is a Windows only package
import sys, os

try:
    from msvcrt import getch  # try to import Windows version
except ImportError:
    def getch():   # define non-Windows version
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def analyze(prefix, playerNum):
    if len(prefix) > 3 and prefix in wordList:
        return ({prefix}, set())
    good, bad = set(), set()
    for possible in hint(prefix):
        tempGood, tempBad = analyze(prefix + possible, playerNum[(playerNum.index(player) + 1)%len(players)])
        if len(tryGood) > 0:
            bad.add(possible)
        else:
            good.add(possible) 
    return good, bad

def challenge(challenger, currPlayer, word):
    global playerColors, players
    chalString = "{}Player {}{}".format(playerColors[challenger], challenger, endColor)
    currString = "{}Player {}{}".format(playerColors[currPlayer], currPlayer, endColor)

    if word in words:
        players[currPlayer] = players[currPlayer] + 1
        print("{} challenges {}!".format(chalString, currString))
        print("'{}' is a word.".format(word))
        print("{} loses and is now a {}{}{}.".format(currString, playerColors[currPlayer], ghost[:players[currPlayer]], endColor))
        return challenger
        
    else:
        print("{} challenges {}!".format(chalString, currString))
        response = input("{}, please enter a word that begins with '{}': ".format(currString, word))
        if response in words:
            print("{} loses and is now a {}{}{}.".format(chalString, playerColors[challenger], ghost[:players[challenger]], endColor))
            return currPlayer
        else:
            print("{} loses and is now a {}{}{}.".format(currString, playerColors[currPlayer], ghost[:players[currPlayer]], endColor))
            return challenger

def start():
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
    print('{} Player game started.'.format(numPlayers))
    print('Terminate with ctrl+D. Press 0 to reset word and ` to clear screen.')
    
    currPlayer = '1'
    while True:
        nextPlayer = None
        
        char = getch()
        
        if char in letters:
            word += char
            print(word)
            
        if char in nums:
            challenger = char
            if challenger == currPlayer:
                print("You cannot challenge yourself.")
                continue
            if len(word) <= 3 and word in words:
                print("Word must be longer than 3 letters in order to be challenged!")
                continue
            nextPlayer = challenge(challenger, currPlayer, word)
            
        if ord(char) == 0x4:
            sys.exit()
            
        elif char == "0":
            word = ""
            print("Word reset.")
            
        elif char == "`":
            os.system('cls' if os.name == 'nt' else 'clear')
        
        if nextPlayer != None:
            currPlayer = nextPlayer
            nextPlayer = None
        else:
            #DETERMINE SUCCESSION!!!
            pass

start()
