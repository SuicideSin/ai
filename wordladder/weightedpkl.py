import sys
import urllib.request
import time
import pickle
start = time.clock()
'''
isNeighbor checks whether or not neighbor neighbor to word. A neighbor is
a word that has only a one letter difference from another word
'''
#
# class vertice:
#     def __init__(self, word, cost):

def isNeighbor(word, neighbor):
    if len(word) != len(neighbor):
        return False
    diffLetters = 0
    consec = False
    for i in range(len(word)):
        # if diffLetters > 1:
        #     break
        if word[i] != neighbor[i]:
            diffLetters += 1
        if word[i-1] != neighbor[i-1] and word[i] != neighbor[i]:
            consec = True
    if diffLetters == 1:
        return 1
    elif diffLetters == 2 and sorted(word) == sorted(neighbor):
        if consec:
	        return 5
        else:
            return -1
    else:
        return -1

file = open('words.txt', 'r')
words = []
wordList = {}
for word in file:
    myWord = word.rstrip("\n")
    words.append(myWord)
    wordList[myWord] = {}

wordCount = 0
edgeCount = 0
for i in words:
    wordCount += 1
    for j in words:
        dist = isNeighbor(i, j)
        #print(type(dist))
        if j > i and dist > 0:
            # wordList[i].append((j, dist) )
            # wordList[j].append((i, dist) )
            wordList[i][j] = dist
            wordList[j][i] = dist
            edgeCount += 1
end = time.clock()

wordList["edges"] = [edgeCount]

fout = open( 'weightedwordladder.pkl' , 'wb' )
pickle.dump( wordList , fout , protocol = 2 )
fout.close()


print(wordList['battle'])
print("Number of words in list :", wordCount)
print("Number of edges in graph :", edgeCount)
if len(sys.argv) > 1:
    argument = sys.argv[1]
    print("Neighbors of", argument, ":", wordList[argument])
print("Completed in", (end-start), "seconds.")
