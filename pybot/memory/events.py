#!/usr/bin/env python
"""
 rael.py        Responses for user events.
 Author:        Rael Garcia <self@rael.io>
 Date:          04/2017
 Tested on:     Python 3 / OS X 10.11.5
"""
import sys


def user_entering(words):

    return "👋"


def user_leaving(words):

    return "👋👋"


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(user_entering(' '.join(sys.argv)))
        print(user_leaving(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
