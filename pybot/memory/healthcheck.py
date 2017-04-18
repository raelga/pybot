#!/usr/bin/env python
"""
 rael.py        Simple healthchecker.
 Author:        Rael Garcia <self@rael.io>
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys


def healthcheck(words):
    "Function to metion me when my name appears in a message"

    if re.search(r'.*Are you ok?.*', words, re.I | re.M):
        return "I'm OK! I'm OK!!"


def hear(words):
    "Implements hear to receive the messages and execute the plugin logic"
    return healthcheck(words)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
