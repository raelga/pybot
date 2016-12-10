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
    'Pkts Battlenet / PSN ID list',
    '----------------------------',
    'Alberto   => alasworld#2665 | Alasworld',
    'Alfonso   => ### | Narcolepsy__',
    'Alex      => Alucard#21141 | Al-ucard',
    'Andrés    => ### | Zariton',
    'Angel     => ### | Angel8Hector',
    'Efrain    => DarkClaymore#2731 | efrain-eu',
    'Fernando  => ### | falcantara13',
    'Guille    => AlNur#2925 | Alnur',
    'Iñigo     => ### | Viciousthekills',
    'Jacko     => JackoRS#2641',
    'Jorge     => ### | Tyryton',
    'Javi      => Berenkaneda#2445',
    'Luisal    => ### | Sysvalve', 
    'Rafa      => Nammoth#2134 | Nammlock',
    'Marcotin  => marcotin#2318 | Marcotin_92 ',
    'Rael      => raelga#2705 | raelga',
    'Raplh     => Nessus7#TBO | Nessus7',
    'Rubén     => ### | ruben_gx',
    'Rubén     => ### | tnife',
    'Sr Snow   => ### | GT_Snow', 
    'Whip1981  => Goliva#2327 | Whip1981',
    'Vero      => ### | Mggartz']

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
