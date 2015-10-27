# -*- coding: cp1252 -*-
import sys
person = “Mom”
if (len(sys.argv) > 1)				#argv is a list, stands for argument vector. argv[0] is the path to the script. 
	person  = sys.argv[1]                   #len(sys.argv) > 1 tests to see if there are two items in argv, the second, argv[1], being the argument
for i in range(len(person)):                    #range(6) -> [0, 1, 2, .... 5]     range(4,8) -> [4, 5, 6, 7]    range(4, 8, 2) -> [4, 6]
    print person[:i] + person[i+1:]             # :i indicates a substring- take all characters up to but not including i. i+1: chops out character at position i
                                                #for string "Mommy", str[5] does not pass, but str[5:] returns and empty string
