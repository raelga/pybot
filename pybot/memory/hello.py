#!/usr/bin/env python
"""
 hello.py       Be polite.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
import sys
import random

DAYS = ['Buenos días', 'Bon dia', 'Good Morning',
        'Egun on', 'Morning', 'Buon giorno',
        'Bonjour', 'Bos días', 'Buenos días arsa',
        'Hola miarma', 'Goede morgen', 'Bom dia',
        'Días buenos a ti también', '\U0001f44b']

NIGHTS = ['Buenas noches', 'Bona nit', 'Good night',
          'Nanit', 'Gute Natch', 'Buonna note',
          'Bonne nuit', 'Goedenacht', 'Boa noite']


def greeting(words):
    "Responds with a random greeting in response to user greetings."

    if any(greeting.lower() in words.lower() for greeting in DAYS):
        return random.choice(DAYS)

    if any(night.lower() in words.lower() for night in NIGHTS):
        return random.choice(NIGHTS)


def hear(words):
    "Implements hear to receive the messages and execute the plugin logic"
    return greeting(words)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
