from collections import *
neighbor = namedtuple('neighbor', ['word', 'cost'])

dict = {'battle':[neighbor('bottle', 1), neighbor('rattle', 0)]}


print(dict)
for word in dict:
    print (dict[word])
    for neighbor in dict[word]:
        print(neighbor.word)
        print(neighbor.cost)
