#!/usr/bin/env python
"""
 cheaptalk.py   Cheap talk, random responses to random input.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys
import random

emojilol = [
            '\U0001f602',
            '\U0001f440',
            '\U0001f617'
            ]

textlol = [
            'lol',
            '(╯°□°）╯︵ ┻━┻)',
             'ay k m lol',
             '(♥_♥)',
             '‎(/.__.)/   \(.__.\)',
             '( ͡° ͜ʖ ͡°)﻿',
             '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. * ･ ｡'
          ]

tellmemore = [
                'Pues al final ha quedado buen día.',
                'Cuéntame más',
                'Me aburrooooooo',
                'Nope',
                'ahá..',
                '\U0001f440'
             ]

botrulz = [ '\U0001f440', '\U0001f60e', '\U0001f60f' ]

def see(photo):

    return { 
            1 : random.choice(emojilol) * random.randint(1,3),
            2 : random.choice(textlol),
            }.get(random.randint(1,16), None)

def hear(words):
    
    if re.search( r'.*skynet.*', words, re.I|re.M):
        return random.choice(botrulz) * random.randint(1,3)

    return { 
            1 : random.choice(tellmemore),
            }.get(random.randinit(1,100), None)

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
        print(see(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
