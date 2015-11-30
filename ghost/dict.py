import sys

file = open('words.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))

import termios
import contextlib
import os
import itertools


@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def main():
    word = ""
    letters = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)]

    print('Terminate with ctrl+C or ctrl+D.')
    print()
    print("Please type in a word: ", end="", flush=True)

    with raw_mode(sys.stdin):
        try:
            while True:
                '''KeyLogger Stuff'''
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break

                '''Ghost Logic'''


                if ch in letters:
                    print(ch, end="",flush=True)
                    word += ch

                if ord(ch) == 0x0a:
                    print("\n",end="")
                    if word in words:
                        print("{} is a valid word.".format(word))
                        print("Definition can be found at http://dictionary.reference.com/browse/{}?s=t".format(word))
                    else:
                        print("'{}' is not a valid word.".format(word))

                    word = ""
                    print()
                    print("Please type in a word: ", end="", flush=True)





        except (KeyboardInterrupt, EOFError):
            print("Game Terminated.")
            pass


main()
