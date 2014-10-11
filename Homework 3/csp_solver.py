__author__ = 'Christopher Raleigh and Anthony Ferrero'

import sys

forward_checking = sys.argv[2]
with open(sys.argv[1], 'r') as problem_file:
    print(problem_file.read())
    print(forward_checking)