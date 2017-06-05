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

EMOJIS = [
    '\U0001f602',
    '\U0001f440',
    '\U0001f617'
]

ASCII_ARTS = [
    'lol',
    '(╯°□°）╯︵ ┻━┻)',
    'ay k m lol',
    '(♥_♥)',
    '‎⨌⨀_⨀⨌',
    '( ͡° ͜ʖ ͡°)﻿',
    '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. * ･ ｡',
    '(っ◕‿◕)っ',
    '( ͡° ͜ʖ ͡°)-︻デ┳═ー',
    'ヽ(￣(ｴ)￣)ﾉ',
    '( ͠° ͟ʖ ͡°)﻿'
]

TEXT = [
    'Pues al final ha quedado buen día.',
    'Cuéntame más',
    'Me aburrooooooo',
    'Nope',
    'ahá..',
    '\U0001f440'
]

SKYNET_EMOJIS = ['\U0001f440', '\U0001f60e', '\U0001f60f']


def choice(message):
    "Listens to choice command and returns a random choice from words."
    return random.choice(message.text.split(' ')[1:])

def coin(words):
    "Listens to coin command and returns a random coin face."
    return random.choice(['heads', 'tails'])
    
def hear(words):
    "Implements hear to receive the messages and execute the plugin logic"

    if re.search(r'.*skynet.*', words, re.I | re.M):
        return random.choice(SKYNET_EMOJIS) * random.randint(1, 3)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
        print(see(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
