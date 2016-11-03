#!/usr/bin/env python
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys
import random

def hear(words):

    if re.search( r'(^|.*)rael(.*|$)', words, re.I|re.M):
        return "@raelga"

    if re.search( r'.*Are you ok?.*', words, re.I|re.M):
        return "I'm OK! I'm OK!!"

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
