#!/usr/local/bin/python3
from itertools import permutations
import time, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4

def board(vec):
    print ("\n".join('. ' * i + '\033[1;32mX\033[0m' + ' .' * (n-i-1) for i in vec) + "\n" + "-"*(2*n-1) + "\n")

solutions = set()

start = time.clock()
cols = range(n)
for vec in permutations(cols):
    if n == len(set(vec[i]+i for i in cols)) == len(set(vec[i]-i for i in cols)):
        solutions.add(vec)
end = time.clock()

for i in solutions:
    print(i)
print("{} solutions in {} seconds.".format(len(solutions), end-start))