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


def salute(words):

    return "👋"

def farewell(words):

    return "👋👋"

def main(argv):
    if len(sys.argv)>1:
        print(salute(' '.join(sys.argv)))
        print(bye(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
