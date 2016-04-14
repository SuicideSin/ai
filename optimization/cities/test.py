#!/usr/local/bin/python3
import math, random, time, sys

def test(i, s):
    print(i)
    print(s)
    for i in range(10000):
        pass
    
def doStuff(f, *args):
    s = time.clock()
    f(*args)
    e = time.clock()
    print(e-s)

doStuff(test, 3, "nice")

l = [1,3,4,5]
print(l)
print(*l)

def t(tup):
    test(*tup)

t((4,2))