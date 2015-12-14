from pickle import load
from time import time
import sys

start = time()

trie = load( open( 'words.pkl' , 'rb' ) )



if len(sys.argv) > 1:
    dic = trie
    for char in sys.argv[1]:
        dic = dic[char]
    print(dic.keys())
    for key in dic:
        print("{}: {}".format(key, dic[key]))
    

end = time()

print("Completed in {} seconds.".format(end-start))