import sys, urllib
link = "http://academics.tjhsst.edu/compsci/ai/words.txt"

hFile = urllib.urlopen(link)
for line in hFile:
    myWord = line.rstrip("\n")

#list/array => [9, "bill", "sue", 10, [10, 2]]
'''
aList = []      .append9
aList = [9]  
'''
#dictionary/associative array => {:Bill":47, "Sue":5, "Bob":16] KEYS ARE UNIQUE, VALUES ARE NOT
'''
aDict = {}
aDict["Bill"] = 47
'''

def diffCount(str1, str2):
    if(len(str1)!=len(str2))
        
'''
ASSIGNMENT
Read in the word list found in the link -
find how many words there are
form a graph with words,
    tell number of edges
    tell number of vertices
take a command line argument, and find out how many neighbors the word has

yclept =to be called
'''
