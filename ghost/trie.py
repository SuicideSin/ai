from pickle import dump
from time import time
import sys

start = time()

filename = "words.txt"

tree = {}
cur = tree

def addWord(word):
	global cur
	if len(word)==0:
		cur[''] = 0;
		cur = tree
		return
	if word[0] in cur.keys():
		cur = cur[word[0]]
	else:
		cur[word[0]] = {}
		cur = cur[word[0]]
	addWord(word[1:])

fin = open(filename).read().splitlines()

for i in fin:
	addWord(i)

fout = open(filename.split(".")[0] + ".pkl", "wb")
dump(tree,fout,protocol = 2)
fout.close()

end = time()

#print(sorted(tree['b']['e'].keys()))
print("Completed in {} seconds.".format(end-start))
