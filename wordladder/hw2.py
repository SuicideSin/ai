import sys, urllib.request, time, pickle
start = time.clock()

wordList = pickle.load( open( 'wordladder.pkl' , 'rb' ) )

freq = {}
freqV = {}
for k in wordList:
    freq[len(wordList[k])] = 0
    freqV[len(wordList[k])] = []
for l in wordList:
    freq[len(wordList[l])] += 1
    freqV[len(wordList[l])].append(l)

edgeCount = wordList.pop("edges")[0]
wordCount = len(wordList)

print("Number of words in list :", wordCount)
print("Number of edges in graph :", edgeCount)
print("Neighborhood size frequency dictionary :", freq)
print("Has the most neighbors :")
for most in freqV[len(freqV)-1]:
    print("\t Word :", most, "| Neighbors :", wordList[most])
end = time.clock()
print("Completed in", (end-start), "seconds.")
