#!/usr/bin/env python
"""
 battletags.py  Battlenet user list.
 Author:        Rael Garcia <self@rael.io>
 Date:          0692016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys
import random

battletags = [
    'Pkts Battlenet ID list',
    '----------------------',
    'Alucard  => Alucard#21141',
    'AlNur    => AlNur#2925',
    'Kaneda   => Berenkaneda#2445',
    'JackoRS  => JackoRS#2641',
    'raelga   => raelga#2705',
    'Efrain   => DarkClaymore#2731',
    'Nammlock => Nammoth#2134',
    'Marcotin => marcotin#2318' ]

def hear(words):

    if re.search( r'^\/battletags.*', words, re.I|re.M):
        return ("\n".join(battletags))


def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
