import sys, urllib.request, time, math, pickle
start = time.clock()

file = open('words.txt', 'r')
words = []
size = 0
for word in file:
    size += 1
    myWord = word.rstrip("\n")
    words.append(myWord)

wordList = {}
for word in words:
    for i in range(0,6):
        if word[:i] + "?" + word[i+1:] not in wordList:
            wordList[word[:i] + "?" + word[i+1:]] = []
            wordList[word[:i] + "?" + word[i+1:]].append(word)
            continue
        else:
            wordList[word[:i] + "?" + word[i+1:]].append(word)

#print(wordList["s?ared"])

edgeCount = 0
for key in wordList:
    n = len(wordList[key])
    if n < 3:
        edgeCount += math.floor(n/2)
    else:
        edgeCount += (n*(n-3)/2) + n



print("{} words in list.".format(size))
print("{} edges in graph.".format(int(edgeCount)))

print("Completed in {} seconds.".format((time.clock()-start)))
