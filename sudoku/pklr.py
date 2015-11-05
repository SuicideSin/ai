import pickle



allGroups = [ [] for i in range(9)]
allSyms = set(str(i) for i in range(1, 10))
cellNeighbors = [ set() for i in range(0, 81) ]
possible = {}

temp = []
boxes = {}
for i in range(0, 81):
    c = i%9
    if allGroups[c] == None:
        allGroups[c] = []
    allGroups[c].append(i)

    if i%9 == 0 and i != 0:
        allGroups.append(temp)
        temp = []
    temp.append(i)
    if i == 80:
        allGroups.append(temp)

    r = int(i/9)
    c = i%9
    rsec = int(r/3)
    csec = int(c/3)
    b = "".join([str(rsec), str(csec)])
    if b not in boxes:
        boxes[b] = []
    boxes[b].append(i)
for box in boxes:
    allGroups.append(boxes[box])

for i in range(0, 81):
    for group in allGroups:
        if i in group:
            temp = set(group)
            cellNeighbors[i] = cellNeighbors[i] | temp

list = []
list.append(allGroups)
list.append(cellNeighbors)

fout = open( 'sets.pkl' , 'wb' )

pickle.dump( list , fout , protocol = 2 )

fout.close()
