#!/usr/bin/env python
"""
 hello.py       Be polite.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import re
import sys
import random

greetings = ['Buenos días', 'Bon dia', 'Good Morning',
                'Egun on', 'Morning', 'Buon giorno',
                'Bonjour', 'Bos días', 'Buenos días arsa',
                'Hola miarma', 'Goede morgen', 'Bom dia',
                'Días buenos a ti también', '\U0001f44b' ]

nights = ['Buenas noches', 'Bona nit', 'Good night',
              'Nanit', 'Gute Natch', 'Buonna note',
              'Bonne nuit','Goedenacht', 'Boa noite']

def greeting(words):

    if any(greeting.lower() in words.lower() for greeting in greetings):
        return random.choice(greetings)

    if any(night.lower() in words.lower() for night in nights):
        return random.choice(nights)

def hear(words):
    return greeting(words)

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
