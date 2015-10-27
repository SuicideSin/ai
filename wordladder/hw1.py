import sys, urllib.request, time, pickle
start = time.clock()
'''
isNeighbor checks whether or not neighbor neighbor to word. A neighbor is
a word that has only a one letter difference from another word
'''
def isNeighbor(word, neighbor):
    if len(word) != len(neighbor):
        return False
    diffLetters = 0
    for i in range(len(word)):
        if diffLetters > 1:
            break
        if word[i] != neighbor[i]:
            diffLetters += 1
    if diffLetters == 1:
        return True
    else:
        return False

file = open('words.txt', 'r')
words = []
wordList = {}
for word in file:
    myWord = word.rstrip("\n")
    words.append(myWord)
    wordList[myWord] = []

wordCount = 0
edgeCount = 0
for i in words:
    wordCount += 1
    for j in words:
        if j > i and isNeighbor(i, j) == True:
            wordList[i].append(j)
            wordList[j].append(i)
            edgeCount += 1
end = time.clock()

wordList["edges"] = [edgeCount]

fout = open( 'wordladder.pkl' , 'wb' )
pickle.dump( wordList , fout , protocol = 2 )
fout.close()

print("Number of words in list :", wordCount)
print("Number of edges in graph :", edgeCount)
if len(sys.argv) > 1:
    argument = sys.argv[1]
    print("Neighbors of", argument, ":", wordList[argument])
print("Completed in", (end-start), "seconds.")
