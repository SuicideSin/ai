def numBoard():
    i = 1
    x = 0
    c = 0
    n = 0
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    while n < 81:
        r = int(i/9)
        c += 1
        if c == 1:
            print("|", end="")
        if len(str(n)) == 1:
            s = str(n) + " "
        else:
            s = str(n)
        print("{}".format(s), end="")

        if c%3 != 0:
            print(" ", end="")


        if c%3 == 0 and x<2:
            x += 1
            print("|", end="")

        if c==9:
            print("|", end="")

        if i%9 == 0:
            c = 0
            x = 0
            if int(i/9)%3==0 and r<9:
                print("\n|--------+--------+--------|")
            else:
                print()

        i += 1
        n += 1
    print("````````````````````````````")
