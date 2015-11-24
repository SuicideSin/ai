import sys

file = open('ghost.txt', 'r')
words = []
for line in file:
    words.append(line.rstrip('\n'))

import termios
import contextlib


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
    nums = "0123456789"
    turn = 0
    numPlayers = 2
    print('2 Player game started.')
    print('Terminate with ctrl+C or ctrl+D.')
    with raw_mode(sys.stdin):
        try:
            while True:
                
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break
                    
                if ch in nums and turn==0 and int(ch) > 2:
                    numPlayers = int(ch)
                    print("Game set to {} players.".format(numPlayers))
                
                if ch not in nums:
                    word = ''.join([word, ch])
                    print(word)
                if ch in nums and int(ch) == 0:
                    print(chr(27) + "[2J")
                turn += 1
                
        except (KeyboardInterrupt, EOFError):
            print("Game Terminated.")
            pass


main()