import sys, time

file = open('words.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))
    
def hint(prefix):
    options = set()
    for word in words:
        if prefix != word and prefix == word[:len(prefix)]:
            options.add(word[len(prefix):len(prefix)+1])
    return options
    

def analyze(prefix, playerNum):
    if len(prefix) > 3 and prefix in words:
        return ({prefix}, set())

    good, bad = set(), set()
    for possible in hint(prefix):
        tempGood, tempBad = analyze(prefix + possible, (playerNum + 1) % 2)
        if len(tempGood) > 0:
            bad.add(possible)
        else:
            good.add(possible) 
    return good, bad

start = time.clock()

if len(sys.argv) < 3:
    good, bad = analyze("", int(sys.argv[1]))
else:
    good, bad = analyze(sys.argv[2], int(sys.argv[1]))

print("Good: {}".format(sorted(good)))
print("Bad: {}".format(sorted(bad)))

end = time.clock()

print("Total time: {} seconds".format(end-start))