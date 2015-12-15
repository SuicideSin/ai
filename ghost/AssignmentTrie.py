"""+==========================+========-========*========-========+==========================+
   ||                        A TRIE CLASS TO BE USED IN THE GHOST LAB                       ||
   ||                           by M. Stueben (December 11, 2012)                           ||
   +==========================+========-========*========-========+==========================+


   Consider the following Python code:

                Dict = {'A':1, 'B':2, 'C':3,}
                Dict['A'] = 1000 # Modify the value of an existing key.
                Dict['D'] = 4    # Insert a new key-and-value.
                print(Dict)      # Output: {'A': 1000, 'B': 2, 'C': 3, 'D': 4}

   Also, if we have a object called x and it has a dictionary (called children) as a class variable, then the
way we insert a letter in the children of x is x.children['A'] = someValue. Hopefully this review will help
you understand how to work with a trie data structure.

   A trie (pronounced "try") is a fundamental abstract data type (ADT) in programming. A trie is a MULTI-
BRANCHED tree that is searched for PATHS to particular nodes, not just the nodes themselves. We will construct
our trie so that its nodes will hold single letters (and links to other letters) but its paths will be words--
at least in some cases. The trie's advantages are a small compression of size (compared to placing every word
in its own node) and a quick retrieval. The word 'trie' comes from the word 'reTRIEve'.

   The main idea of a trie is to insert each individual letter of a word effficiently into a tree structure.
Consequently, all words that start with the letter 'a' pass through the SAME node ('a') of the trie. All words
that begin with "ab" will pass through the same first two nodes of the trie. As the letters of an input word
are extracted from the word and placed into the tree, the input word becomes shorter, eventually becoming the
empty string (''). In that case a '$' is appended as a child node of the terminal letter in the trie. This
indicates the completion of a word in the trie. An example will make this clear.

    Below is a trie with the words CAT, CATS, CATNIP, CATNAP, CAT-X, and CAN'T. This allows 29 characters to
be represented by 19 characters. Try to find all six words (each followed by a $) in the tree below.

                                               * <--the root node
                                               |
                                               C
                                               |
                                               A        <--CAN does NOT appear, but CAT does appear.
                                               |           Why? Because of the placement of the '$'
                                    {T---------+--------N} symbols.
                                     |                  |
                            {S-------N------X------$}   T
                             |       |      |           |
                             $   {I--+--A}  $           $
                                  |     |
                                  P     P
                                  |     |
                                  $     $

            1. Add CAT.    Then  3 chars are represented by  4 chars: 4/3   = 1.33.
            2. Add CATS.   Then  7 chars are represented by  6 chars: 6/7   = 0.86.
            3. Add CATNIP. Then 13 chars are represented by 10 chars: 10/13 = 0.77.
            4. Add CATNAP. Then 19 chars are represented by 13 chars: 13/19 = 0.68.
            5. Add CAT-X.  Then 24 chars are represented by 16 chars: 16/24 = 0.67.
            6. Add CAN'T.  Then 29 chars are represented by 19 chars: 19/29 = 0.65.

   The more words that are entered into the trie, the more efficient the trie becomes in its storage. However,
the memory saving is not why we use a trie. We use it for its fast look-up time. In our trie, we will ignore
apostrophes and hyphens. We also ignore words with numbers--e.g., "7-up". The only non-lowercase character we
use is "$". One way to build a trie is to use a Node class to hold a value and a dictionary of links to other
nodes. Here is my code to create such a Node object. Consequently, the trie will be constructed by linking
node objects together.

           +-------------------------------------DEFINITION------------------------------------+
           |  class Node(object):                                                              |
           |      def __init__ (self, value):                                                  |
           |          self.value     = value                                                   |
           |          self.children  = {}     # example: {'a':Node('a'), 'b':Node('b'), etc.}  |
           +-----------------------------------------------------------------------------------+

    We can build the trie and insert "cat" with these two lines:

                                       +-----------------------+
(1)                                    |  root = Node('*')     |
(2)                                    |  root.insert('cat')   | <--We have to create an insert method, first.
                                       +-----------------------+

   The first line creates a place in memory that holds the value (*), and holds an empty dictionary called
children. The instruction root = Node('*') gives us this:

(3)                                   self.value     = '*' # self = root
(4)                                   self.children  = {}  # self = root

   That was easy, because it follows from the definition of Node. The KEYS of the dictionary will later be
lowercase letters like 'a', 'b', etc. Their VALUES will be Nodes that have the SAME letter value--e.g.,

                          {'c': Node('c'), 'g': Node('g'),'n': Node('n'),}

   If you can understand how the next line works, you will understand everything about trie coding. The in-
struction
                                       root.insert('cat')

will try to insert 'c', 'a', 't', and '$' into the trie (starting at the root Node) by RECURSION. Notice that
the insert call needs a node (later referred to as self) and a string:

                                 +-----------------------------+
                                 | someNode.insert(someString) | <-- IMPORTANT! (someNode = self)
                                 +-----------------------------+

   We set stng = 'cat'. It is possible that 'c' (= stng[0]) is already in the trie as a first letter. So we
ask

(5)                             if stng[0] in self.children.keys(): ...

   which is the same as

(6)                             if stng[0] in self.children: ...

   If stng[0] in self.children.keys() is true, then we move to the node associated with the dictionary key
stng[0], and recursively start over. We do this with this line:

(7)                         self.children[stng[0]].insert(stng[1:])

   But suppose 'c' was NOT one of root's children. In other words, suppose 'c' is not a key in the root (=
self) dictionary. Again, suppose that stng[0] in self.children.keys() is False. In that case, we create a Node
to contain the value 'c', and stuff that Node in to the root dictionary. Then we move to that Node and try to
insert the 'a':

(8)                            if stng[0] not in self.children.keys():

(9)                            p = Node(stng[0])
(10)                           self.children[p.value] = p  # p.value  = 'c'
(11)                           p.insert(stng[1:])          # stng[1:] = 'at'

   Finally, there is a third case. Suppose we place 'c', 'a', and 't' in the dictionary. Then stng has become
empty: stng = ''. In that case you create a Node with the value '$' (p = Node('$')) and then append it to the
dictionary of the 't' node with

(12)                       self.children[p.value] = p. # p.value = '$'

  If these 12 lines make sense, then you understand the details and can write the insert function for the trie
program. [Note on November 7, 2014: I wrote this program two years ago, and have just reviewed this worksheet.
Almost none of this code makes any sense to me. I use classes so rarely that I forget the details of working
with them. All I can say is that when I did understand this code, I thought this explanation was clear. So
perhaps the first step is to re-read this explanation several times. The second step is to write a little of
the code and then try to print out the trie.] Good luck.

ASSIGNMENT: Write the code to build a trie. Use a Node class. You need class methods to

    1. construct a Node class with a character value and a dictionary of links.
    2. Instantiate a root node with character '*'
    3. insert words into the trie. (I have indicated how you might do steps 1-3 above.)
    4. print all words in Trie. (This is up to you to figure out.)
    5. search to find a word, returning True or False. (This is also up to you to figure out.)

The following is some of my code:


##############################################<START OF PROGRAM>##############################################
class Node(object):
#-------------------------------------------------------------------------------
    def __init__ (self, value):
        self.value     = value
        self.children  = {}     # Example: {'a':Node('a'), 'b':Node('b'), etc.}
#-------------------------------------------------------------------------------------------------Node-class--
    def __repr__(self): # Both node.print() and print(node) call the same code,
        self.print()    # which is in the print method below.
        return ''
#-------------------------------------------------------------------------------------------------Node-class--
    def print(self, stng): # Recursively print all words in the Trie.
        ???
#-------------------------------------------------------------------------------------------------Node-class--
    def display(self):    #  This is a (recursive) utility I used for for debugging.
        if self.value == '$': return
     #--print data
        print ('========== NODE ==========')
        print ('--> self.value     =', self.value)
        print ('--> self.children: [', end = '')

      #--print values of node's children
        for key in self.children:
            if key != '$':
               print (key, sep ='', end = ', ')
        print (']')
        print('---------------------------')

     #--RECURSIVELY print the node's children
        for char in self.children:
            (self.children[char]).display()
#-------------------------------------------------------------------------------------------------Node-class--
    def insert(self, stng): # recursive
        ???
#-------------------------------------------------------------------------------------------------Node-class--
    def search(self, stng): # recursive
        ???
#############################################<END OF NODE CLASS>##############################################

#===================================<GLOBAL CONSTANTS and GLOBAL IMPORTS>=====================================

from sys import setrecursionlimit; setrecursionlimit(100) # default = 1000.
from time import clock
#===================================================<MAIN>====================================================

def main():
    root = Node('*')
    root.insert('cat')
    root.insert('catnip')
    root.insert('cats')
    root.insert('catnap')
    root.insert("can't") # <-- Note the double quotes.
    root.insert('cat-x')
    root.insert('dog')
    root.insert('dogs')
    root.insert('dognip')
    root.print ('')
    root.display()       # <-- Useful for debugging.
    print('SEARCH:', root.search('junk'))
    printElapsedTime()
#-------------------------------------------------------------------------------------------------------------
def printElapsedTime():
    print('\n---Total run time =', round(clock() - startTime, 2), 'seconds.')
#-------------------------------------------------------------------------------------------------------------
if __name__ == '__main__': startTime = clock(); main()
###############################################<END OF PROGRAM>###############################################
"""


#                                             TEACHER'S SOLUTION
##############################################<START OF PROGRAM>##############################################
class Node(object):

    def __init__ (self, value):
        self.value     = value  # is either a lower-case letter or a '$'
        self.children  = {}     # Example: {'a':Node('a'), 'b':Node('b'), etc.}
#-------------------------------------------------------------------------------------------------Node-class--

    def __repr__(self): # Both node.print() and print(node) call the same code.
        self.print()
        return ''
#-------------------------------------------------------------------------------------------------Node-class--

    def print(self, stng): # recursively print All words
        if self.value == '$':
            print (stng[:-1]) # The -1 will avoid printing the '$'.
            return
        for ch in self.children:
            stngCopy = stng + ch
            self.children[ch].print(stngCopy) # recursive call
#-------------------------------------------------------------------------------------------------Node-class--

    def display(self, level):    #  This is a (recursive) utility used for for debugging.
        if self.value == '$': return

     #--print data
        print ('========== NODE ========== level =', level)
        print ('--> self.value     =', self.value)
        print ('--> self.children: [', end = '')

      #--print values of node's children
        for key in self.children:
            if key != '$':
               print (key, sep ='', end = ', ')
        print (']')
        print()

     #--RECURSIVELY print the node's children
        for char in self.children:
            level += 1
            (self.children[char]).display(level)
#-------------------------------------------------------------------------------------------------Node-class--

    def insert(self, stng): # recursive

    #---case 1. Insert termination character '$'
        if stng == '':
           self.children['$'] = Node('$')
           return

    #--case 2. If the initial character (stng[0]) is NOT one of the children, then insert the character
    #          into the children dictionary and recurse with the remainder of the string.
        if stng[0] not in self.children:
           p = Node(stng[0])
           self.children[stng[0]] = p
           p.insert(stng[1:])

    #--case 3. Since stng[0] is already in the children dictionary, recurse and insert the rest of the string.
        self.children[stng[0]].insert(stng[1:])
#-------------------------------------------------------------------------------------------------Node-class--

    def search(self, stng): # recursive
        #--case 1. final letter is found in trie
           if len(stng) == 0:
              if '$' in self.children:
                 return True
              else:
                 return False
        #--case 2. current letter in not in trie
           if stng[0] not in self.children:
               return False

        #--case 3. go on  to look at the next letter.
           return self.children[stng[0]].search (stng[1:])
##############################################<END OF NODE CLASS>#############################################

#===================================<GLOBAL CONSTANTS and GLOBAL IMPORTS>=====================================
from sys import setrecursionlimit; setrecursionlimit(100) # default = 1000.
from time import clock
#===================================================<MAIN>====================================================
def main():
    root = Node('*')
    root.insert('cat')
    root.insert('catnip')
    root.insert('dogs')
    root.insert('cats')
    root.insert('catnap')
    root.insert("can't")
    root.insert('cat-x')
    root.insert('dog')
    root.insert('dognip')
    root.print('*') # This instruction prints all the words in the trie.
    print('SEARCH:', root.search("cat")) # True
    print('SEARCH:', root.search("ca"))  # False
#-------------------------------------------------------------------------------------------------------------
if __name__ == '__main__': from time import clock; startTime = clock(); main();
print ('-'*24, '\nRun time =', round(clock()-startTime, 2), 'seconds.')
###############################################<END OF PROGRAM>###############################################
"""

QUIZ 1. Create a node class that accepts a single character as a "value"
        and builds an empty dictionary of "children" (4 lines).

        Hint: See below.

    class _______________:

        def __init__ (_____________):

            ________________________

            ________________________

ANSWER 1.
class Node(object):
    def __init__ (self, value):
        self.value     = value
        self.children  = {}
==============================================================================================================

QUIZ 2. Given the insert function below, write the single line of code that
        will insert a node with value '$' into the current node's children.
        The current node is called self. [You MUST underline any capital
        letters.]

    def insert(self, stng):
        if stng == '':
            _______________________________________ (Fill in.)
            return
        ...

ANSWER 2.
    def insert(self, stng): # recursive
    #---case 1. Insert termination character '$'
        if stng == '':
           self.children['$'] = Node('$') # <-- ANSWER
           return               ^
==============================================================================================================

QUIZ 3. Given the insert function below, write the several lines of code that will insert
        a node with with the initial character of stng into the current node's children.
        Then, recursively call the insert function with the remainder of stng (excluding
        the first character).


    def insert(self, stng): # recursive
    #---case 1. Insert termination character '$'
        ...
    #--case 2. If the initial character (stng[0] ) is NOT one of the children, then insert
    #          the character into the children dictionary and recurse with the remainder
    #          of the string. [Introduce the varialble p.]
        if stng[0] not in self.children:

           ______________________________________

           ______________________________________

           ______________________________________
           return


ANSWER 3.
    def insert(self, stng): # recursive
    #--If the initial character (stng[0] ) is NOT one of the children, then insert
    #  the character into the children dictionary and recurse with the remainder
    #  of the string.

        if stng[0] not in self.children:
           p = Node(stng[0])                # <-- ANSWER
           self.children[stng[0]] = p       # <-- ANSWER
           p.insert(stng[1:])               # <-- ANSWER
           return
==============================================================================================================
QUIZ 4.
    def insert(self, stng): # recursive
    #--Since stng[0] is already in the children dictionary, recurse and
       insert the rest of the string into the trie.

ANSWER 4.
    def insert(self, stng): # recursive
    #---case 1.
        ...
    #--case 2.
        ...
    #--case 3. Since stng[0] is already in the children dictionary, recurse and insert the rest of the string.

        self.children[stng[0]].insert(stng[1:]) # <--ANSWER
==============================================================================================================

FINAL QUIZ 5: Write the recursive insert function. We reference the Node class given below.

class Node(object):
    def __init__ (self, value):
        self.value     = value
        self.children  = {}
#-------------------------------------------------------------------------------------------------Node-class--

    def insert(self, stng): # recursive

    #---case 1. Insert termination character '$' if it needs to be inserted.
        ???

    #--case 2. If the initial character (stng[0] ) is NOT one of the children, then insert the character
    #          into the children dictionary and recurse with the remainder of the string.
        ???

    #--case 3. Since stng[0] is already in thr children dictionary, recurse and insert the rest of the string.
        ???

ANSWER 5. See Code.
"""