''''''''''''''''''''''''''''
'''First Ghost Assignment''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
1. Read in the words from ghost.txt, argument to script indicates number of players (default is two)
2. Implement a keystroke monitor-- process is different for windows, mac, and linux -- perhaps make a class that is ready for any system (use sys.platform)
    > CAT
    Keystroke monitor!! Enter key doesn't get pressed
4. A number indicates a challenger number
     Script will adjudicate the challenge
     Will output the loser in the scenario, adds to player's ghost, restarts
5. A period will cause the script to show all possible available letters on the next line that could be played that. If dot is inputted and there are no available letters, game ends with no loser
    ex:
        > cat.
        ... s, h, t, a, e, f
        > cat    #waiting for next input
     
     
    
    
'''


''''''''''''''''''''''''
''''''Due Thurs''''''''
'''''''''''''''''''''''
Create a new file to do this one

1. python3 ghost 2 c   #means that a computer joins the game
   python3 ghost 2 c c 3 #means that the first 2 players are human, next 2 are computers, and the next 3 are people
   
   
2. The computer will play and pick amongst the hints to play

if the computer finds that it cannot play a word without losing, it should challenge
'''

   
   
''''''''''''''''''''''''''''
'''''''Due Mon'''''''''''''
'''''''''''''''''''''''''
TRIES!!!!
https://en.wikipedia.org/wiki/Trie

Recursive function that makes the computer play perfectly




'''''''''''''''''''''''''''''''
Making the computer smarter



First off, probably want to use a Trie (a.k.a. Prefix tree)
Second off, probably want to use recursion

Recursive function returns a tuple of good (force win) and bad letters.
    Function terminates if prefix is a word!!
    Initialization:
        Set of good letters and a set of bad letters, start off empty

    Recursive part:
        For each possible letter, recurse
        Get back a temporary good set and a temporary bad set
        
        If temp good is empty, implies put possible letter in good
        else its bad for us and put it in bad

        return good and bad :)

        this shit aint a freebie tho. big help tho. structure is given, but we have to implement it exactly.
        

def analyze(prefix, playerNum):
    if len(prefix) > 3 and prefix in wordList:
        return ({prefix}, set())
    good, bad = set(), set()
    for possible in hint(prefix):
        tryGood, tryBad = analyze(prefix + possible, playerNum[(playerNum.index(player) + 1)%len(players)])
        if len(tryGood) > 0:
            bad.add(possible)
        else:
            good.add(possible) 
    return good, bad

TRIES!!!

def buildTrie( prefix, wordIterator ):
    myDic = {}
    for word in wordIterator:
        
        if prefix in wordIterator: myDic[''] = {}
        
        if len(word) < 4: continue
        if word[:len(prefix)] != prefix: continue
        if word[len(prefix)] not in myDic:
            myDic[word[len(prefix)]] = set()
        myDic[word[len(prefix)]].add(word)
        for ltr in myDic:
            myDic[ltr] = buildTrie(prefix + ltr, myDic[ltr])
        
        return myDic

def analyze(prefix, playerNum, okayerCh)
    if playerNum == 0











