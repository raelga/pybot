#!/usr/bin/env python
"""
 rael.py        Pesonal stuff.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Tested on:     Python 3 / OS X 10.11.5
"""

import random


def _get_cat_gif():
    "Get a random cat from catapi"

    cat_apiurl = "http://thecatapi.com/api/images/get?format=src&type=gif"
    return cat_apiurl + "&timestamp=" + str(random.random()) + ".gif"


def cat():
    "Returns the groups menu for the command shortcut `groups`."

    return _get_cat_gif()


def main():
    "This allows to execute the plugin in standalone mode"
    print(cat())


if __name__ == "__main__":
    main()
