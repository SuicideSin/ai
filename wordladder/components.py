import sys, urllib.request, time
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

def bfs(s, adj):
    level = {s: 0}
    parent = {s: None}
    i = 1
    frontier = [s]
    while frontier:
        next = []
        for u in frontier:
            for v in adj[u]:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1
    return len(level)

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

checked = []
freq = {}
max = 0
for k in wordList:
    if k not in checked:
        checked.append(k)
        for l in wordList[k]:
            checked.append(l)
        kLength = bfs(k, wordList)
        if kLength not in freq:
            freq[kLength] = 1
        else:
            freq[kLength] += 1
        if kLength > max:
            max = kLength

print("Number of words in list :", wordCount)
print("Number of edges in graph :", edgeCount)
print("Compenent size frequency dictionary :", freq)
print(max, len(freq))
end = time.clock()
print("Completed in", (end-start), "seconds.")
