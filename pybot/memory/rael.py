#!/usr/bin/env python
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys


def rael_utils(words):
    "Function to metion me when my name appears in a message"

    if re.search(r'(^|\s)rael(\s|$)', words, re.I | re.M):
        return "@raelga"


def hear(words):
    "Implements hear to receive the messages and execute the plugin logic"
    return rael_utils(words)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
